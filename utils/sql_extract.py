#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runs sql query given the SQL and database URI
"""
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import csv
import os
import codecs
import cStringIO
from prod_categorization.utils.logger import logger


# run sql query
def sql_extract(country, sql_query, sqlalchemy_db_uri, output_dir, query_type):

    # create engine, session, and connection
    engine = create_engine(sqlalchemy_db_uri, pool_recycle=10800, encoding='utf8')
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    logger.debug(sql_query)

    # extract records (put SQL query here)
    # conn.execute('set global max_allowed_packet=2048000')  # enlarge max_allowed_packet of mysql server
    output_path = output_dir + '/' + query_type + '_' + country + '.csv'

    # Execute SQL
    df = pd.read_sql(sql_query, conn)
    logger.info('Data fetched for: {}'.format(country))

    # Save dataframe
    df.to_csv(output_path, index=False, encoding='utf8')
    logger.info('Data saved for: {}'.format(country))
