from django.shortcuts import render, HttpResponse
from .models import CustomerDetails
from .serialization import searialization_class, searialize_rest_detail, searialize_rest_timingss, \
    searialize_menu_details
from .models import CustomerDetails, RestaurantDetail, RestTimingss, MenuDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Count, Max
from django.db import transaction
from datetime import datetime
from django.db import connection
import pymysql
import json
from django.contrib.auth.models import User


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
    # , request2, request3, request4
    print(request1.query_params)
    # datetime_str = request1.GET.get('datetime')
    # day_index = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").weekday()
    # time = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M").time()
    # print(day_index, time)

    # return HttpResponse("Show Restaurants!!!!!")

    if request1.method == 'GET' and request1.GET.get('top') is None:
        # query_set = 0
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
    print(request1.query_params)
    price_range_list = request1.GET.get('price_range').split('-')
    # print(request1.GET.get('lesser_than'))
    # return HttpResponse("Show Top Restaurants!!!!!!!!!!")
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


# @api_view(['GET'])
# def show_top_restaurants1(request1, request2, request3, request4, request5, request6, request7):
#     if request1.method == 'GET':
#         menu_object = (MenuDetails.objects.filter(menu_price__gte=request4) & MenuDetails.objects.filter(
#             menu_price__lte=request6)).values('restaurant').annotate(total=Count('dish_name')).filter(
#             total__gt=request3)
#         rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
#             '-cash_balance')[:int(request2)]
#         ser = searialize_rest_detail(rest_det, many=True)
#         return Response(rest_det.values('restaurant_name'))


# @api_view(['GET'])
# def show_top_restaurants2(request1, request2, request3, request4, request5, request6, request7):
#     if request1.method == 'GET':
#         menu_object = (MenuDetails.objects.filter(menu_price__gte=request4) & MenuDetails.objects.filter(
#             menu_price__lte=request6)).values('restaurant').annotate(total=Count('dish_name')).filter(
#             total__lt=request3)
#         rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by(
#             '-cash_balance')[:int(request2)]
#         return Response(rest_det.values('restaurant_name'))


@api_view(['GET', 'POST'])
def place_order(request):
    # print(request.query_params)
    if request.method == 'GET':
        user_id = int(request.GET.get('user_id'))
        dish_name = request.GET.get('dish_name')
        restaurant_name = request.GET.get('restaurant_name')
        user_info_query = CustomerDetails.objects.filter(customer_id=user_id)
        restaurant_details_query = RestaurantDetail.objects.filter(restaurant_name=restaurant_name)
        dish_and_restaurant_query = MenuDetails.objects.filter(dish_name=dish_name) & MenuDetails.objects.filter(
            restaurant__in=restaurant_details_query.values('restaurant_id'))
        # print(restaurant_details_query)
        # print(dish_and_restaurant_query.values('menu_price'))
        # print(type(user_info_query.values('cash_balance')))
        #
        # print(len(CustomerDetails.objects.filter(cash_balance__gte=dish_and_restaurant_query.values('menu_price')) & user_info_query))
        # return HttpResponse("Hellllllllllo")

        if len(user_info_query) == 1 and len(dish_and_restaurant_query) == 1:
            if len(CustomerDetails.objects.filter(cash_balance__gte=dish_and_restaurant_query.values('menu_price')) & user_info_query) == 1:
                try:
                    with transaction.atomic():
                        # print("HElllll")
                        user_details = CustomerDetails.objects.get(customer_id=user_id)
                        restaurant_details = RestaurantDetail.objects.get(restaurant_name=restaurant_name)
                        dish_and_restaurant_details = MenuDetails.objects.get(dis_name=dish_name, restaurant_id=restaurant_details.restaurant_id)
                        transaction_datetime_str = datetime.now().strptime('%Y-%m-%d %H:%M')
                        transaction_datetime = datetime.strptime(transaction_datetime_str, '%Y-%m-%d %H:%M')

                        print("HEGRHTH:- ", user_details.customer_id)

                        # dt = CustomerDetails.objects.get(customer_id=1000)
                        # dt.cash_balance = dt.cash_balance + 50
                        # dt.save(update_fields=['cash_balance'])
                        # dt.save()
                        return Response("Transaction successsfulll!!!!!")
                except:
                    return Response("Transaction unsuccessful!!!!!!")
            return Response("Insufficient Cash Balance!!!!!!!!")
        return Response("Wrong request!!!!!!!!!")

        # return HttpResponse("Bahooot badhiyaaaaaaaaa!!!!")

# @api_view(['GET', 'POST'])
# # @transaction.atomic()
# def add_name(request):
#     name_of_record = request.GET.get('name')
#     if request.method == 'GET':
#         print(request.query_params)
#         # return HttpResponse("Hello world!!!!!!!!")
#         # return Response("Hellllllllllll")
#         # with transaction.commit():
#         try:
#             with transaction.atomic():
#                 det = CustomerDetails(1000, customer_name=name_of_record, cash_balance=50.00)
#                 det.save()
#                 return Response("Record added!!!!!!!!!!!!")
#         except:
#             return Response("Record can't be added!!!!!!!!!")
#         # print(CustomerDetails.objects.aggregate(Max('customer_id')))
#         # return Response("Record added!!!!!")
