from loguru import logger
from .alchemy import Base

try:

    sales_txn = Base.classes.sales_txn
    o_site = Base.classes.o_site

except Exception as err:
    logger.error("error while creating models - {}".format(err))
