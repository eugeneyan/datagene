"""
Runs sql query given the SQL and database URI
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import csv
import os
import datetime
from logger import logger


# run sql query
def sql_extract(country, sql_query, sqlalchemy_db_uri, output_dir, query_type):

    # create engine, session, and connection
    engine = create_engine(sqlalchemy_db_uri, pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    session = Session
    conn = engine.connect()
    logger.debug(sql_query)

    # extract records (put SQL query here)
    records = conn.execute(text(sql_query))
    logger.info('Data fetched for: {}'.format(country))

    # save to csv
    fh = open(output_dir + '/' + query_type + '_' + country + '.csv', 'wb')
    outcsv = csv.writer(fh)

    # write column headers
    outcsv.writerow(records.keys())

    # write rows
    outcsv.writerows(records)
    logger.info('Data saved for: {}'.format(country))

    fh.close()
