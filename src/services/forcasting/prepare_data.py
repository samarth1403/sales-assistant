from prophet import Prophet
from src.db import get_raw_db
import pandas as pd
import psycopg2.extras
from datetime import datetime

def prepare_data(store_code: str = None ):
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
            cursor.execute(query, {'store_code': store_code})
        else:
            query = """
                SELECT st.bill_time::date as ds, SUM(st.amount) as y FROM sales_txn st 
                GROUP BY st.bill_time::date
                ORDER BY st.bill_time::date;
            """
            cursor.execute(query)
        data = cursor.fetchall()
        if not data:
            raise ValueError(f"No data found for store code: {store_code}")

        # Converting the data to a DataFrame and prepare it for Prophet
        df = pd.DataFrame(data)
        df['ds'] = pd.to_datetime(df['ds'])
        df['y'] = df['y'].astype(float)

        # Adding Holidays
        holidays = pd.DataFrame({
            'ds': pd.to_datetime([
                '2023-01-01',  # New Year
                '2023-01-26',  # Republic Day
                '2023-08-15',  # Independence Day
                '2023-10-02',  # Gandhi Jayanti
                '2023-11-01',  # Diwali (tentative)
                '2023-12-25',  # Christmas
            ]),
            'holiday': [
                'New Year', 'Republic Day', 'Independence Day',
                'Gandhi Jayanti', 'Diwali', 'Christmas'
            ]
        })

        # df['cap'] = df['y'].max() * 1.2  # set a reasonable upper bound
        df['floor'] = 0  # sales can't go below zero

        # Initialize Prophet model with holidays
        model = Prophet(holidays=holidays, daily_seasonality=True,
                        weekly_seasonality=True, yearly_seasonality=True,
                        growth="logistic"
                        )
        model.fit(df)

        future = model.make_future_dataframe(periods=365)
        # future['cap'] = df['cap'].max()
        future['floor'] = 0

        forecast = model.predict(future)

        forecast[['yhat', 'yhat_lower', 'yhat_upper']] = forecast[['yhat', 'yhat_lower', 'yhat_upper']].clip(lower=0).round(0).astype(int)

        # Prevent scientific notation when displaying
        pd.set_option('display.float_format', '{:.0f}'.format)

        # Prepare the final DataFrame with predictions
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

        for _, row in forecast.iterrows():
            cursor.execute("""
                        INSERT INTO sales_forcast (site_code, date ,predicted, predicted_lower, predicted_upper, is_deleted, created_time, updated_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (store_code,row['date'], row['yhat'], row['yhat_lower'], row['yhat_upper', 0, str(datetime.now()), str(datetime.now())]))

        rdb.flush()
        rdb.commit()
        print("Data forcasting done successfully.")

    except Exception as e:
        raise ValueError(f"Error fetching data for store code {store_code}: {e}")


if __name__ == "__main__":
    prepare_data(store_code='E099')