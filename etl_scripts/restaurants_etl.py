import json
import os
import re
import pymysql
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

HOST_NAME = os.environ.get('HOST_NAME')
USER_NAME = os.environ.get('USER_NAME')
USER_PASS = os.environ.get('USER_PASS')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


def get_index_of_day(temp_str):  # returns the index corresponding to the day name.
    return_value = 0

    if temp_str.find('mon') != -1:  # for monday 0 will be returned
        return_value = 0
    elif temp_str.find('tue') != -1:  # for tuesday 1 will be returned
        return_value = 1
    elif temp_str.find('wed') != -1:  # for wednesday 2 will be returned
        return_value = 2
    elif temp_str.find('thu') != -1:  # for thursday 3 will be returned
        return_value = 3
    elif temp_str.find('fri') != -1:  # for friday 4 will be returned
        return_value = 4
    elif temp_str.find('sat') != -1:  # for saturday 5 will be returned
        return_value = 5
    elif temp_str.find('sun') != -1:  # for sunday 6 will be returned
        return_value = 6

    return return_value


def checking_for_day_range(days_str):  # this function's work is to check whether there is day range or not and
    # return the result accordingly
    day_num_list = []

    if days_str.find('-') >= 0:  # this gets executed when the days_str is in range format, eg:- Mon - Fri
        t_list = days_str.split('-')
        day_num_list.append(get_index_of_day(t_list[0]))
        day_num_list.append(get_index_of_day(t_list[1]))
    else:  # this gets executed when days_str is just a day, eg:- Tues
        day_num_list.append(get_index_of_day(days_str))

    return day_num_list


def convert_time_str_to_datetime(temp_list):  # helps in converting the time in string format to datetime format
    start_time, end_time = temp_list[0].strip(), temp_list[1].strip()  # start_time means the opening time of
    # restaurant, end_time means the closing time of restaurant
    final_value = []  # here the datetime format time gets stored

    if start_time.find(':') == -1:  # this checking is done to see time strings where only hour is written
        temp_start_time_obj = datetime.strptime(start_time, '%I%p').time()
        final_value.append(temp_start_time_obj)
    else:  # this part gets executed when there is hour part and minutes part in the time string
        temp_start_time_obj = datetime.strptime(start_time, '%I:%M%p').time()
        final_value.append(temp_start_time_obj)

    if end_time.find(':') == -1:  # this checking is done to see time strings where only hour is written
        temp_end_time_obj = datetime.strptime(end_time, '%I%p').time()
        final_value.append(temp_end_time_obj)
    else:  # this part gets executed when there is hour part and minutes part in the time string
        temp_end_time_obj = datetime.strptime(end_time, '%I:%M%p').time()
        final_value.append(temp_end_time_obj)

    return final_value


def get_timings_of_each_day(day_timings_str_list):  # this function helps in getting the timings of each day
    day_timings_list = [[]] * 7  # this list stores the timings of each day

    for item_str in day_timings_str_list:
        item_str = item_str.strip()
        first_num_pos = re.search('[0-9]', item_str)  # here I am finding the position of the first digit so that I
        # can get name of the days and timings of those days after splitting from that position

        timings_str = item_str[first_num_pos.start():].replace(' ', '').split('-')  # this gives me the timings string
        days_str = item_str[0: first_num_pos.start()].strip()  # this gives the days name
        days_str = days_str.lower()  # converting it lowercase for easy comparison
        timings_list = convert_time_str_to_datetime(timings_str)  # getting the converted time string

        days_str_list = days_str.split(',')  # getting the list of days

        for day in days_str_list:
            day_num_list = checking_for_day_range(day)  # getting the indexes of days entered in range format or just
            # the day

            if len(day_num_list) == 2:  # if the length of list is 2 then it means the string was in range format
                if day_num_list[0] < day_num_list[1]:  # this gets executed when the index of starting day is less
                    # than index of ending day
                    for i in range(day_num_list[0], day_num_list[1] + 1):  # because of this loop we are able to get
                        # timings for the days
                        day_timings_list[i] = timings_list
                else:  # this gets executed when the index of starting day is more than index of ending day
                    for i in range(day_num_list[0], day_num_list[1] + 8):
                        day_timings_list[i % 7] = timings_list
            else:  # this is executed when we encounter only a single day
                day_timings_list[day_num_list[0]] = timings_list

    return day_timings_list


def splitting_the_opening_hours(opening_hours_str):  # this function splits the opening hours string and returns the
    # opening hours of each day as a list of list of datetime
    day_timings_str_list = opening_hours_str.split('/')
    timings_value_list = get_timings_of_each_day(day_timings_str_list)

    return timings_value_list


def main():
    restaurant_data_path = os.path.realpath('restaurant_with_menu.json')  # gets the relative path of restaurant_with_menu.json
    restaurant_data_file = open(restaurant_data_path, encoding="utf-8")  # opening the restaurant_data_path
    restaurant_data = json.load(restaurant_data_file)  # loading the restaurant_data_path to read it as json

    connection_instance = pymysql.connect(host=HOST_NAME, user=USER_NAME, password=USER_PASS, database=DATABASE_NAME)  # # enter your database's credentials
    cursor_instance = connection_instance.cursor()  # creating a cursor instance of connection_instance

    try:
        create_restaurant_detail_table = "CREATE TABLE restaurant_detail (restaurant_id int NOT NULL , restaurant_name varchar(255) NOT NULL, cash_balance DOUBLE,PRIMARY KEY (restaurant_id))"  # query for creating restaurant_detail
        cursor_instance.execute(create_restaurant_detail_table)  # executing the above query
        connection_instance.commit()  # committing the above query

        create_rest_timingss_table = "CREATE TABLE rest_timingss (id int NOT NULL AUTO_INCREMENT, restaurant_id int NOT NULL, day_num int NOT NULL, opening_time TIME DEFAULT NULL, closing_time TIME DEFAULT NULL, PRIMARY KEY (id), FOREIGN KEY (restaurant_id) REFERENCES restaurant_detail(restaurant_id))"  # query for creating rest_timingss
        cursor_instance.execute(create_rest_timingss_table)  # executing the above query
        connection_instance.commit()  # committing the above query

        create_menu_details = "CREATE TABLE menu_details (menu_id int NOT NULL AUTO_INCREMENT, restaurant_id int NOT NULL, dish_name varchar(1000) NOT NULL, menu_price DOUBLE, PRIMARY KEY (menu_id), FOREIGN KEY (restaurant_id) REFERENCES restaurant_detail(restaurant_id))"  # query for creating menu_details
        cursor_instance.execute(create_menu_details)  # executing the above query
        connection_instance.commit()  # committing the above query

        try:
            restaurant_id = 1  # making restaurant_id as 1 and will be inserting this value in the restaurant_id
            # column of restaurant_detail
            insert_in_restaurant_detail_table = "INSERT INTO restaurant_detail (restaurant_id, restaurant_name, cash_balance) VALUES (%s, %s, %s)"  # query for inserting record in restaurant_detail
            for details in restaurant_data:
                cursor_instance.execute(insert_in_restaurant_detail_table,(restaurant_id, details['restaurantName'], details['cashBalance']))  # inserting the records in the restaurant_detail
                connection_instance.commit()  # commting the above query
                restaurant_id += 1  # incrementing the value of restaurant_id
        except:  # executes if you are not able to insert record in restaurant_detail table
            print("Can't insert record in restaurant_detail table")

        try:
            restaurant_id = 1  # making restaurant_id as 1 and will be inserting this value in the restaurant_id
            # column of menu_details
            insert_in_menu_details_table = "INSERT INTO menu_details (restaurant_id, dish_name, menu_price) VALUES (%s, %s, %s)"  # query for inserting record in menu_details
            for details in restaurant_data:
                for food_item in details['menu']:
                    cursor_instance.execute(insert_in_menu_details_table,(restaurant_id, food_item['dishName'], food_item['price']))  # inserting the records in the menu_details
                    connection_instance.commit()  # committing the above query
                restaurant_id += 1  # incrementing the above query
        except:  # executes if you are not able to insert record in menu_details table
            print("Can't insert record in menu_details table")

        try:
            restaurant_id = 1  # making restaurant_id as 1 and will be inserting this value in the restaurant_id
            # column in rest_timingss
            insert_in_rest_timingss_table = "INSERT INTO rest_timingss (restaurant_id, day_num, opening_time, closing_time) VALUES (%s, %s, %s, %s)"  # query for inserting record in rest_timingss
            for details in restaurant_data:
                timings_list = splitting_the_opening_hours(details['openingHours'])
                for day_index in range(0, 7):  # this is to insert the records for each day for each restaurant
                    if len(timings_list[day_index]) == 2:  # this executes when the restaurant is open on the
                        # particular day
                        cursor_instance.execute(insert_in_rest_timingss_table, (restaurant_id, day_index, timings_list[day_index][0], timings_list[day_index][1]))  # inserting records in the rest_timingss
                        connection_instance.commit() # committing the above query
                    else:  # this executes when the restaurant is not open on the particular day
                        cursor_instance.execute(insert_in_rest_timingss_table, (restaurant_id, day_index, -1, -1))
                        # inserting records in the rest_timingss and adding -1 in opening and closing time to signify
                        # that it is closed on that particular day
                        connection_instance.commit()  # committing the above query
                restaurant_id += 1  # incrementing the restaurant_id
            print("Tables created successfully")
        except:  # executes when we can't insert record in rest_timingss
            print("Can't insert record in rest_timingss table")
    except:  # executes when we can't create tables
        print("Can't create tables")
    finally:
        restaurant_data_file.close()
        connection_instance.close()


main()
