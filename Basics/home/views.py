from django.shortcuts import render, HttpResponse
from .models import CustomerDetails
from .serialization import searialization_class, searialize_rest_detail, searialize_rest_timingss, \
    searialize_menu_details
from .models import CustomerDetails, RestaurantDetail, RestTimingss, MenuDetails, PurchaseHistory
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Count, Max
from django.db import transaction
from datetime import datetime
from django.db import connection
import pymysql
import json
from django.contrib.auth.models import User


def calculate_edit_distance(search_str, result_str):
    search_str, result_str = search_str.lower(), result_str.lower()
    length_of_search_str = len(search_str)
    length_of_result_str = len(result_str)

    dp_array = [[0 for x in range(0, length_of_search_str + 1)] for y in range(0, length_of_result_str + 1)]

    for i in range(0, length_of_search_str + 1):
        dp_array[0][i] = i

    for j in range(0, length_of_result_str + 1):
        dp_array[j][0] = j

    for i in range(1, length_of_result_str + 1):
        for j in range(1, length_of_search_str + 1):
            if result_str[i - 1] != search_str[j - 1]:
                dp_array[i][j] = min(dp_array[i - 1][j], dp_array[i][j - 1], dp_array[i - 1][j - 1]) + 1
            else:
                dp_array[i][j] = dp_array[i - 1][j - 1]

    return dp_array[length_of_result_str][length_of_search_str]


# Create your views here.
def index(request):
    # print(request)
    context = {"variable": "var is the value"}
    return render(request, 'index.html', context)
    # return HttpResponse("This is the home page!!!!!")


def about(request):
    return HttpResponse("This is the about page!!!!!")


def services(request):
    return HttpResponse("This is the services page!!!!!")


def contacts(request):
    posts = CustomerDetails.objects.all()
    print(posts)
    return render(request, 'contacts.html', {'post': posts})
    # return HttpResponse("This is contacts page!!!!!!!!!")


@api_view(['GET'])
def show_customer_details(request):
    print(request.query_params)
    return HttpResponse('This is show customer details!!!!!!')
    # if request.method == 'GET':
    #     results = CustomerDetails.objects.all()
    #     serialize = searialization_class(results, many=True)
    #     return Response(serialize.data)


@api_view(['GET'])
def show_restaurants(request1):
    # print(request1.query_params)

    if request1.method == 'GET' and request1.GET.get('top') is None:
        datetime_str = request1.GET.get('datetime')
        day_index = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").weekday()
        time = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").time()
        open_restaurants = RestTimingss.objects.filter(day_num=day_index) & RestTimingss.objects.filter(
            opening_time__lte=time) & RestTimingss.objects.filter(closing_time__gte=time)
        rest_det = RestaurantDetail.objects.filter(restaurant_id__in=open_restaurants.values('restaurant'))
        serialize2 = searialize_rest_detail(rest_det, many=True)

        return Response(serialize2.data)
    elif request1.method == 'GET' and request1.GET.get('greater_than') is not None:
        price_range_list = request1.GET.get('price_range').split('-')
        num_of_top_restaurants = int(request1.GET.get('top'))
        dishes_threshold = int(request1.GET.get('greater_than'))
        lower_price = float(price_range_list[0])
        higher_price = float(price_range_list[1])

        menu_object = (MenuDetails.objects.filter(menu_price__gte=lower_price) & MenuDetails.objects.filter(
            menu_price__lte=higher_price)).values('restaurant').annotate(total=Count('dish_name')).filter(
            total__gt=dishes_threshold)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
            '-cash_balance')[:num_of_top_restaurants]

        return Response(rest_det.values('restaurant_name'))

    elif request1.method == 'GET' and request1.GET.get('lesser_than') is not None:
        price_range_list = request1.GET.get('price_range').split('-')
        num_of_top_restaurants = int(request1.GET.get('top'))
        dishes_threshold = int(request1.GET.get('lesser_than'))
        lower_price = float(price_range_list[0])
        higher_price = float(price_range_list[1])

        menu_object = (MenuDetails.objects.filter(menu_price__gte=lower_price) & MenuDetails.objects.filter(
            menu_price__lte=higher_price)).values('restaurant').annotate(total=Count('dish_name')).filter(
            total__lt=dishes_threshold)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
            'cash_balance')[:num_of_top_restaurants]

        return Response(rest_det.values('restaurant_name'))


@api_view(['GET'])
def top_restaurants(request1):
    # print(request1.query_params)
    price_range_list = request1.GET.get('price_range').split('-')
    if request1.method == 'GET' and request1.GET.get('greater_than') is not None:
        num_of_top_restaurants = int(request1.GET.get('top'))
        dishes_threshold = int(request1.GET.get('greater_than'))
        lower_price = float(price_range_list[0])
        higher_price = float(price_range_list[1])

        menu_object = (MenuDetails.objects.filter(menu_price__gte=lower_price) & MenuDetails.objects.filter(
            menu_price__lte=higher_price)).values('restaurant').annotate(total=Count('dish_name')).filter(
            total__gt=dishes_threshold)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
            '-cash_balance')[:num_of_top_restaurants]

        return Response(rest_det.values('restaurant_name'))

    elif request1.method == 'GET' and request1.GET.get('lesser_than') is not None:
        num_of_top_restaurants = int(request1.GET.get('top'))
        dishes_threshold = int(request1.GET.get('lesser_than'))
        lower_price = float(price_range_list[0])
        higher_price = float(price_range_list[1])

        menu_object = (MenuDetails.objects.filter(menu_price__gte=lower_price) & MenuDetails.objects.filter(
            menu_price__lte=higher_price)).values('restaurant').annotate(total=Count('dish_name')).filter(
            total__lt=dishes_threshold)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
            'cash_balance')[:num_of_top_restaurants]

        return Response(rest_det.values('restaurant_name'))


@api_view(['GET'])
def relevant_restaurants(request):
    restaurant_name = request.GET.get('name')
    query_parameter = "%" + restaurant_name + "%"
    if request.method == 'GET':
        raw_sql_query = RestaurantDetail.objects.raw(
            'SELECT restaurant_id, restaurant_name FROM restaurant_detail WHERE restaurant_name LIKE %s',
            [query_parameter])

        edit_distance_dict = {}

        for record in raw_sql_query:
            edit_distance = calculate_edit_distance(restaurant_name, record.restaurant_name)
            edit_distance_dict[record.restaurant_name] = edit_distance

        final_dict = dict(sorted(edit_distance_dict.items(), key=lambda x: x[1]))
        # print(final_dict)

        return Response(final_dict.keys())


@api_view(['GET'])
def relevant_dishes(request):
    dish_name = request.GET.get('name')
    query_parameter = "%" + dish_name + "%"
    # print(par)
    if request.method == 'GET':
        raw_sql_query = MenuDetails.objects.raw(
            'SELECT DISTINCT(dish_name), menu_id FROM menu_details WHERE dish_name LIKE %s', [query_parameter])

        edit_distance_dict = {}

        for record in raw_sql_query:
            edit_distance = calculate_edit_distance(dish_name, record.dish_name)
            edit_distance_dict[record.dish_name] = edit_distance

        final_dict = dict(sorted(edit_distance_dict.items(), key=lambda x: x[1]))

        return Response(final_dict.keys())


@api_view(['GET', 'POST'])
def place_order(request):
    if request.method == 'GET':
        user_id = int(request.GET.get('user_id'))
        dish_name = request.GET.get('dish_name')
        restaurant_name = request.GET.get('restaurant_name')
        user_info_query = CustomerDetails.objects.filter(customer_id=user_id)
        restaurant_details_query = RestaurantDetail.objects.filter(restaurant_name=restaurant_name)
        dish_and_restaurant_query = MenuDetails.objects.filter(dish_name=dish_name) & MenuDetails.objects.filter(
            restaurant__in=restaurant_details_query.values('restaurant_id'))

        if len(user_info_query) == 1 and len(dish_and_restaurant_query) == 1:
            if len(CustomerDetails.objects.filter(
                    cash_balance__gte=dish_and_restaurant_query.values('menu_price')) & user_info_query) == 1:
                try:
                    with transaction.atomic():
                        user_details = CustomerDetails.objects.get(customer_id=user_id)
                        restaurant_details = RestaurantDetail.objects.get(restaurant_name=restaurant_name)
                        dish_and_restaurant_details = MenuDetails.objects.get(dish_name=dish_name,
                                                                              restaurant=restaurant_details.restaurant_id)

                        transaction_datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M')
                        transaction_datetime = datetime.strptime(transaction_datetime_str, '%Y-%m-%d %H:%M')

                        user_details.cash_balance -= dish_and_restaurant_details.menu_price
                        restaurant_details.cash_balance += dish_and_restaurant_details.menu_price
                        new_transaction_record = PurchaseHistory.objects.create(customer_id=user_id,
                                                                                dish_name=dish_name,
                                                                                restaurant_name=restaurant_name,
                                                                                transaction_amount=dish_and_restaurant_details.menu_price,
                                                                                transaction_date=transaction_datetime)
                        # print("*******", new_transaction_record.transaction_id)
                        user_details.save(update_fields=['cash_balance'])
                        restaurant_details.save(update_fields=['cash_balance'])
                        user_details.save()
                        restaurant_details.save()
                        new_transaction_record.save()
                        return Response("Transaction successful")
                except:
                    return Response("Transaction unsuccessful!!!!!!")
            return Response("Insufficient Cash Balance!!!!!!!!")
        return Response("The dish!!!!!!!!!")
