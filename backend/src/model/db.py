from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
import subprocess

DATABASE = 'mysql+pymysql'
USER = 'creist'
PASSWORD = os.environ['MYSQL_PASSWORD']
HOST = '127.0.0.1'
PORT = '3307'
DB_NAME = 'flask_sv'

CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

engine = create_engine(CONNECT_STR)

Base = declarative_base()
