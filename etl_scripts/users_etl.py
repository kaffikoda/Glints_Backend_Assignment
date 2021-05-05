import os
import json
from datetime import datetime
import pymysql
from dotenv import load_dotenv

load_dotenv()

HOST_NAME = os.environ.get('HOST_NAME')
USER_NAME = os.environ.get('USER_NAME')
USER_PASS = os.environ.get('USER_PASS')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


def change_transaction_date(temp_str):  # this function changes the time in string format to time in datetime format
    temp_str = temp_str.strip()
    return datetime.strptime(temp_str, '%m/%d/%Y %I:%M %p')


def main():
    users_purchase_history_path = os.path.realpath('users_with_purchase_history.json')  # getting the relative path of the users_with_purchase_history.json
    users_purchase_history_file = open(users_purchase_history_path, encoding="utf-8")  # opening the users_purchase_history_path
    data = json.load(users_purchase_history_file)  # loading it so that we can read it

    connection_instance = pymysql.connect(host=HOST_NAME, user=USER_NAME, password=USER_PASS, database=DATABASE_NAME)  # enter your database's credentials

    try:
        cursor_instance = connection_instance.cursor()  # creating a cursor instance of connection_instance
        create_customer_details_table = "CREATE TABLE customer_details (customer_id int NOT NULL, customer_name varchar(255) NOT NULL, cash_balance DOUBLE, PRIMARY KEY (customer_id))"  # sql query for creating customer_details table
        cursor_instance.execute(create_customer_details_table)  # executing the above query
        create_purchase_history_table = "CREATE TABLE purchase_history (transaction_id INT NOT NULL AUTO_INCREMENT, customer_id INT NOT NULL, dish_name varchar(1000), restaurant_name varchar(255), transaction_amount DOUBLE, PRIMARY KEY (transaction_id), transaction_date DATETIME, FOREIGN KEY (customer_id) REFERENCES customer_details (customer_id))"
        # sql query for creating purchase_history table
        cursor_instance.execute(create_purchase_history_table)  # executing the above query

        try:
            insert_in_customer_details_table = "INSERT INTO customer_details (customer_id, customer_name, cash_balance) VALUES (%s, %s, %s)"  # query for inserting record in customer_details table
            insert_in_purchase_history_table = "INSERT INTO purchase_history (customer_id, dish_name, restaurant_name, transaction_amount, transaction_date) VALUE (%s, %s, %s, %s, %s)"  # query for inserting record in purchasing_history table

            for details in data:
                cursor_instance.execute(insert_in_customer_details_table, (details['id'], details['name'], details['cashBalance']))  # inserting details of each customer in the table
                connection_instance.commit()  # committing the above query

                for purchases in details['purchaseHistory']:  # this is for inserting the purchase history of each
                    # customer in the purchase_history table
                    time_stamp = change_transaction_date(purchases['transactionDate'])  # getting the tansaction date
                    # time in the datetime format
                    cursor_instance.execute(insert_in_purchase_history_table, (details['id'], purchases['dishName'], purchases['restaurantName'], purchases['transactionAmount'], time_stamp))  # inserting the record in the purchase_history table
                    connection_instance.commit()  # committing the above query
            print("Tables created successfully")  # printing the table successfully created message
        except:  # this executes when we are not able to insert a record
            print("Can't add records in the table")
    except:  # this executes when we are not able to create table
        print("Can't create tables")
    finally:
        connection_instance.close()  # closing the connection instance
        users_purchase_history_file.close()  # closing the users_purchase_history_file


main()
