import json
from math import ceil
from src.services.sql_query_generator.generate_query import generate_sql_query
from src.services.forcasting.generate_forecasting_query import (
    generate_forecasting_sql_query,
)
from src.services.sql_query_executer.sql_query_executer import sql_query_executer
from src.services.contextual_query.params_extraction.get_extracted_params import get_extracted_params
from src.services.contextual_query.comparative_sql_query_generator.generate_comparative_sql_query import generate_comparative_sql_query
from src.services.response_formatter.generate_response import generate_response
from src.services.normal_response_formatter.generate_normal_response import (
    generate_normal_response,
)
from src.services.other_questions.get_other_questions_answer import get_other_questions_answer
from src.services.query_classifier.classify import classify_query
from fastapi import APIRouter, Depends, HTTPException, Query, Body, FastAPI
from uvicorn import run
from src.db import get_db, get_raw_db
from fastapi.middleware.cors import CORSMiddleware
from src.db.alchemy_models import sales_txn
from sqlalchemy.orm import Session
from loguru import logger
import psycopg2.extras
import pandas as pd
from prophet import Prophet
from datetime import datetime
from src.services.vector_store.pinecone_client import search_similar_context, upsert_texts
from src.services.followup_handler.get_followup_question import get_followup_question


def main():
    print("🔍 Sales Query Classifier")
    print("Type your query below (type 'exit' to quit):\n")

    while True:
        user_input = input("📝 Query: ").strip()
        output = ""
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting classifier.")
            break

        previous_context_results = search_similar_context(user_input, session_id='default')
        print(len(previous_context_results))
        if len(previous_context_results) > 0:
            previous_context = "\n\n".join([result.page_content for result in previous_context_results])
            user_input = get_followup_question(previous_context, user_input)
        classification = classify_query(user_input)
        print(f"📊 Classification: {classification}\n")
        if classification == "sql_query":
            sql_query = generate_sql_query(user_input)
            output = sql_query_executer(sql_query, user_input)
        elif classification == "forecasting_query":
            sql_query = generate_forecasting_sql_query(user_input)
            output = sql_query_executer(sql_query, user_input)
        elif classification == "contextual_query":
            extracted_params = get_extracted_params(user_input)
            extracted_params = json.loads(extracted_params.replace('```json', '').replace('```', ''))
            output = generate_comparative_sql_query(extracted_params["metric"],extracted_params["trend"],extracted_params["time_period"],extracted_params["previous_time_period"])
        else:
            output = get_other_questions_answer(user_input)
            print("❗ Unknown query type. Please try again.\n")

        qa_pair = f"User:{user_input}\nAssistant:{output}\n"
        metadata = {"session_id" : "default"}
        upsert_texts([qa_pair], [metadata], session_id="default")
        print(f"Output : {output}")

def insert_forcasting_data_for_store(store_code: str = None):
    # First of all we will get the daily data from the database to train the model
    rdb = next(get_raw_db())
    cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        if store_code:
            query = """
              SELECT
                  st.bill_time::date as ds,
                  SUM(st.amount) as y
              FROM sales_txn st
              WHERE st.store_code = %(store_code)s
              GROUP BY st.bill_time::date, st.store_code
              ORDER BY st.bill_time::date;
            """
            cursor.execute(query, {"store_code": store_code})
        else:
            query = """
                SELECT st.bill_time::date as ds, SUM(st.amount) as y FROM sales_txn st 
                GROUP BY st.bill_time::date
                ORDER BY st.bill_time::date;
            """
            cursor.execute(query)
        data = cursor.fetchall()
        if not data:
            return

        # Converting the data to a DataFrame and prepare it for Prophet
        df = pd.DataFrame(data)
        df["ds"] = pd.to_datetime(df["ds"])
        df["y"] = df["y"].astype(float)

        # Adding Holidays
        holidays = pd.DataFrame(
            {
                "ds": pd.to_datetime(
                    [
                        "2023-01-01",  # New Year
                        "2023-01-26",  # Republic Day
                        "2023-08-15",  # Independence Day
                        "2023-10-02",  # Gandhi Jayanti
                        "2023-11-01",  # Diwali (tentative)
                        "2023-12-25",  # Christmas
                    ]
                ),
                "holiday": [
                    "New Year",
                    "Republic Day",
                    "Independence Day",
                    "Gandhi Jayanti",
                    "Diwali",
                    "Christmas",
                ],
            }
        )

        df["cap"] = df["y"].max() * 1.2  # set a reasonable upper bound
        df["floor"] = 0  # sales can't go below zero

        # Initialize Prophet model with holidays
        model = Prophet(
            holidays=holidays,
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            growth="logistic",
        )
        model.fit(df)

        future = model.make_future_dataframe(periods=365)
        future["cap"] = df["cap"].max()
        future["floor"] = 0

        forecast = model.predict(future)

        forecast[["yhat", "yhat_lower", "yhat_upper"]] = (
            forecast[["yhat", "yhat_lower", "yhat_upper"]]
            .clip(lower=0)
            .round(0)
            .astype(int)
        )

        # Prevent scientific notation when displaying
        pd.set_option("display.float_format", "{:.0f}".format)

        # Prepare the final DataFrame with predictions
        print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))

        for _, row in forecast.tail(365).iterrows():
            cursor.execute(
                """
                        INSERT INTO sales_forecast (site_code, date ,predicted, predicted_lower, predicted_upper, is_deleted, created_time, updated_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                (
                    store_code,
                    str(row["ds"]),
                    row["yhat"],
                    row["yhat_lower"],
                    row["yhat_upper"],
                    0,
                    str(datetime.now()),
                    str(datetime.now()),
                ),
            )
        rdb.commit()
        print("Data forcasting done successfully.")

    except Exception as e:
        raise ValueError(f"Error fetching data for store code {store_code}: {e}")


def insert_forcasting_data():
    rdb = next(get_raw_db())
    cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = """select site_code from o_site where is_deleted = 0"""
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            insert_forcasting_data_for_store(row["site_code"])
    except Exception as e:
        raise ValueError(f"Error inserting forecasting data: {e}")


app = FastAPI(title="CMS V2 Admin Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/ask")
def answer_the_question(question : str ,db: Session = Depends(get_db), rdb: Session = Depends(get_raw_db)):
    try:
        user_input = question.strip()
        output = ""

        previous_context_results = search_similar_context(user_input, top_k=1, session_id='default')
        print(len(previous_context_results))
        if len(previous_context_results) > 0:
            previous_context = "\n\n".join([result.page_content for result in previous_context_results])
            user_input = get_followup_question(previous_context, user_input)
        classification = classify_query(user_input)
        print(f"📊 Classification: {classification}\n")
        if classification == "sql_query":
            sql_query = generate_sql_query(user_input)
            output = sql_query_executer(sql_query, user_input)
        elif classification == "forecasting_query":
            sql_query = generate_forecasting_sql_query(user_input)
            output = sql_query_executer(sql_query, user_input)
        elif classification == "contextual_query":
            extracted_params = get_extracted_params(user_input)
            extracted_params = json.loads(extracted_params.replace('```json', '').replace('```', ''))
            output = generate_comparative_sql_query(extracted_params["metric"], extracted_params["trend"],
                                                    extracted_params["time_period"],
                                                    extracted_params["previous_time_period"])
        else:
            output = get_other_questions_answer(user_input)

        qa_pair = f"User:{user_input}\nAssistant:{output}\n"
        metadata = {"session_id": "default"}
        upsert_texts([qa_pair], [metadata], session_id="default")
        return {
            "answer": output,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

if __name__ == "__main__":
    # main()
    # insert_forcasting_data()
    logger.info("Started main")
    run("main:app", host="0.0.0.0", port=8085, reload=True)
