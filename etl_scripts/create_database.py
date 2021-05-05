import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

HOST_NAME = os.environ.get('HOST_NAME')
USER_NAME = os.environ.get('USER_NAME')
USER_PASS = os.environ.get('USER_PASS')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


def main():
    connection_instance = pymysql.connect(host=HOST_NAME, user=USER_NAME, password=USER_PASS)

    try:
        cursor_instance = connection_instance.cursor()
        create_database_query = "CREATE DATABASE " + DATABASE_NAME
        cursor_instance.execute(create_database_query)
    except:
        print("Can't create database")
    finally:
        connection_instance.close()


main()
