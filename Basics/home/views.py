from django.shortcuts import render, HttpResponse
from .serialization import searialize_restaurant_detail, serializing
from .models import CustomerDetails, RestaurantDetail, RestTimingss, MenuDetails, PurchaseHistory
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from django.db import transaction
from datetime import datetime


def calculate_edit_distance(search_str, result_str):  # through this function I am calculating edit distance of the
    # search term to the name of the restaurant
    search_str, result_str = search_str.lower(), result_str.lower()  # converting the string to lowercase
    length_of_search_str = len(search_str)  # getting length of search term
    length_of_result_str = len(result_str)  # getting length of restaurant name

    dp_array = [[0 for x in range(0, length_of_search_str + 1)] for y in range(0, length_of_result_str + 1)]  #
    # making a 2D array of dimension (length_of_result_str + 1) x (length_of_search_str + 1)

    for i in range(0, length_of_search_str + 1):  # initialising the dp_array
        dp_array[0][i] = i

    for j in range(0, length_of_result_str + 1):  # initialising the dp_array
        dp_array[j][0] = j

    for i in range(1, length_of_result_str + 1):  # assigning values to each combination od string
        for j in range(1, length_of_search_str + 1):
            if result_str[i - 1] != search_str[j - 1]:  # executes when two characters are not equal
                dp_array[i][j] = min(dp_array[i - 1][j], dp_array[i][j - 1], dp_array[i - 1][
                    j - 1]) + 1  # minimum steps of the 3 (insertion, deletion, replacement) and add 1 to it
            else:  # executes when two characters are different
                dp_array[i][j] = dp_array[i - 1][j - 1]

    return dp_array[length_of_result_str][length_of_search_str]  # returns the edit distance


# Create your views here.
def index(request):
    return HttpResponse("This is the index page!!!!!")


@api_view(['GET'])
def restaurants(request):  # it's function is to get the details of the restaurant according to the parameters
    # passed through url
    if request.method == 'GET' and request.GET.get('top') is None:  # this is executed when you want to get the
        # restaurants open on a particular datetime
        datetime_str = request.GET.get('datetime')  # this is to get the datetime passed through the url
        day_index = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").weekday()  # this helps in getting the day
        # index of of the date
        time = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").time()  # this helps us in getting the time part in
        # the datetime url

        open_restaurants = RestTimingss.objects.filter(day_num=day_index, opening_time__lte=time,
                                                       closing_time__gte=time)  # through this we get the restaurant id which are open during that time and day index
        restaurant_detail = RestaurantDetail.objects.filter(
            restaurant_id__in=open_restaurants.values('restaurant'))  # through this we get the details of restaurant
        restaurant_detail_serialized = searialize_restaurant_detail(restaurant_detail,
                                                                    many=True)  # here we do serialization to get the required data, i.e the name of the restaurants

        return Response(restaurant_detail_serialized.data)

    elif request.method == 'GET' and request.GET.get('greater_than') is not None:
        price_range_list = request.GET.get('price_range').split('-')  # we get the price range parameters in a list
        num_of_top_restaurants = int(
            request.GET.get('top'))  # to get the number of top restaurants the user wants to see
        dishes_threshold = int(request.GET.get('greater_than'))  # to get the threshold above which the total dishes
        # in the given price range needs to be
        lower_price = float(price_range_list[0])  # to get the lower value in the price range
        higher_price = float(price_range_list[1])  # to get the greater value in the price range

        menu_details = MenuDetails.objects.filter(menu_price__gte=lower_price, menu_price__lte=higher_price).values(
            'restaurant').annotate(total_dishes_in_price_range=Count('dish_name')).filter(
            total_dishes_in_price_range__gt=dishes_threshold)
        # through this query we are getting the list of restaurants which have dishes more than the given threshold
        # in the given price range

        restaurant_details = (RestaurantDetail.objects.filter(
            restaurant_id__in=menu_details.values('restaurant'))).order_by('-cash_balance')[:num_of_top_restaurants]
        # here we are getting the top restaurants according to the cash balance, i.e more the cash balance more will
        # be it's popularity

        restaurant_details_serialized = searialize_restaurant_detail(restaurant_details, many=True)  # here we do
        # serialization to get the required data, i.e the name of the restaurants

        return Response(restaurant_details_serialized.data)

    elif request.method == 'GET' and request.GET.get('lesser_than') is not None:
        price_range_list = request.GET.get('price_range').split('-')  # we get the price range parameters in a list
        num_of_top_restaurants = int(
            request.GET.get('top'))  # to get the number of top restaurants the user wants to see
        dishes_threshold = int(request.GET.get('lesser_than'))  # to get the threshold below which the total dishes in
        # the given price range needs to be
        lower_price = float(price_range_list[0])  # to get the lower value in the price range
        higher_price = float(price_range_list[1])  # to get the greater value in the price range

        menu_details = MenuDetails.objects.filter(menu_price__gte=lower_price, menu_price__lte=higher_price).values(
            'restaurant').annotate(total_dishes_in_price_range=Count('dish_name')).filter(
            total_dishes_in_price_range__lt=dishes_threshold)
        # through this query we are getting the list of restaurants which have dishes less than the given threshold
        # in the given price range

        restaurant_details = (RestaurantDetail.objects.filter(
            restaurant_id__in=menu_details.values('restaurant'))).order_by('-cash_balance')[:num_of_top_restaurants]
        # here we are getting the top restaurants according to the cash balance, i.e more the cash balance more will
        # be it's popularity

        restaurant_details_serialized = searialize_restaurant_detail(restaurant_details, many=True)  # here we do
        # serialization to get the required data, i.e the name of the restaurants

        return Response(restaurant_details_serialized.data)


@api_view(['GET'])
def relevant_restaurants(request):  # this helps use in getting restaurants ranked by relevance to search term
    restaurant_search_term = request.GET.get('name')  # this helps in getting the restaurant's name
    query_parameter = "%" + restaurant_search_term + "%"  # preparing the search term for the sql query
    if request.method == 'GET':
        raw_sql_query = RestaurantDetail.objects.raw(
            'SELECT restaurant_id, restaurant_name FROM restaurant_detail WHERE restaurant_name LIKE %s',
            [query_parameter])  # through this sql query we get the records of the restaurants which has the search
        # term in their name

        edit_distance_dict = {}  # creating an empty dictionary to store the restaurant name as key and the edit
        # distance of the search term with it as value

        for record in raw_sql_query:  # adding the restaurant name as the key and the edit distance of the search
            # term with it as value
            edit_distance = calculate_edit_distance(restaurant_search_term, record.restaurant_name)
            edit_distance_dict[record.restaurant_name] = edit_distance

        final_dict = dict(sorted(edit_distance_dict.items(), key=lambda x: x[1]))  # sorting the obtained list in
        # ascending order with respect to the values in the dictionary and then converting the obtained tuple into
        # dictionary

        return Response(final_dict.keys())  # returning the obtained keys of the dictionary as response


@api_view(['GET'])
def relevant_dishes(request):  # this helps use in getting dishes ranked by relevance to search term
    dish_search_term = request.GET.get('name')  # this helps in getting the dish's name
    query_parameter = "%" + dish_search_term + "%"  # preparing the search term for the sql query
    if request.method == 'GET':
        raw_sql_query = MenuDetails.objects.raw(
            'SELECT DISTINCT(dish_name), menu_id FROM menu_details WHERE dish_name LIKE %s',
            [query_parameter])  # through this sql query we get the records of the dishes which has the search
        # term in their name

        edit_distance_dict = {}  # creating an empty dictionary to store the dish name as key and the edit distance
        # of the search term with it as value

        for record in raw_sql_query:  # adding the dish name as the key and the edit distance of the search
            # term with it as value
            edit_distance = calculate_edit_distance(dish_search_term, record.dish_name)
            edit_distance_dict[record.dish_name] = edit_distance

        final_dict = dict(sorted(edit_distance_dict.items(), key=lambda x: x[1]))  # sorting the obtained list in
        # ascending order with respect to the values in the dictionary and then converting the obtained tuple into
        # dictionary

        return Response(final_dict.keys())  # returning the obtained keys of the dictionary as response


@api_view(['GET', 'POST'])
def place_order(request):  # this helps in placing the order
    if request.method == 'GET':
        user_id = int(request.GET.get('user_id'))  # getting the user id
        dish_name = request.GET.get('dish_name')  # getting the dish name
        restaurant_name = request.GET.get('restaurant_name')  # getting the name of the restaurant from where you
        # need to place the order
        # user_info_queryset = CustomerDetails.objects.filter(customer_id=user_id)  # getting the query set of the user
        # who is placing the order
        user_info_queryset = CustomerDetails.objects.filter(customer_id=user_id)
        restaurant_details_query = RestaurantDetail.objects.filter(restaurant_name=restaurant_name)  # getting the
        # query set of the restaurant from where you want to place order
        dish_and_restaurant_queryset = MenuDetails.objects.filter(dish_name=dish_name,
                                                                  restaurant__in=restaurant_details_query.values(
                                                                      'restaurant_id'))  # getting the queryset of the dish in the restaurant

        if len(user_info_queryset) == 1 and len(dish_and_restaurant_queryset) == 1:  # this executes only when the
            # userid is valid and the the dish is in the menu of the restaurant
            if len(CustomerDetails.objects.filter(cash_balance__gte=dish_and_restaurant_queryset.values(
                    'menu_price')) & user_info_queryset) == 1:  # this executes only when the user's cash balance of the user is greater than equal to the price of the dish
                try:
                    with transaction.atomic():  # doing atomic transaction with the help of context manager
                        user_details = CustomerDetails.objects.get(customer_id=user_id)  # getting the user details
                        restaurant_details = RestaurantDetail.objects.get(restaurant_name=restaurant_name)  # getting
                        # the restaurant details
                        dish_and_restaurant_details = MenuDetails.objects.get(dish_name=dish_name,
                                                                              restaurant=restaurant_details.restaurant_id)  # getting the record of the dish in the restaurant

                        transaction_datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M')  # converting the
                        # transaction to string in required format
                        transaction_datetime = datetime.strptime(transaction_datetime_str, '%Y-%m-%d %H:%M')  #
                        # converting the string time in datetime format

                        user_details.cash_balance -= dish_and_restaurant_details.menu_price  # deducting the dish
                        # price from user's cash balance
                        restaurant_details.cash_balance += dish_and_restaurant_details.menu_price  # adding the dish
                        # price to the restaurant's cash balance
                        new_transaction_record = PurchaseHistory.objects.create(customer_id=user_id,
                                                                                dish_name=dish_name,
                                                                                restaurant_name=restaurant_name,
                                                                                transaction_amount=dish_and_restaurant_details.menu_price,
                                                                                transaction_date=transaction_datetime)  # creating a new transaction record
                        user_details.save(
                            update_fields=['cash_balance'])  # saving the changes made in the cash balance of the user
                        restaurant_details.save(update_fields=[
                            'cash_balance'])  # saving the changes made in the cash balance of the restaurant
                        new_transaction_record.save()  # saving the new transaction
                        return Response("Transaction successful!")
                except:
                    return Response("Transaction unsuccessful!")  # if transaction fails then this is displayed
            return Response("Insufficient Cash Balance!")  # returned when user's cash balance is less than the
            # dish's price
        return Response("The dish is not present in the restaurant!")  # returned when the dish is not present in the
        # restaurant
