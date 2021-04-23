from django.shortcuts import render, HttpResponse
from .models import CustomerDetails
from .serialization import searialization_class, searialize_rest_detail, searialize_rest_timingss, searialize_menu_details
from .models import CustomerDetails, RestaurantDetail, RestTimingss, MenuDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
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
    if request.method == 'GET':
        results = CustomerDetails.objects.all()
        serialize = searialization_class(results, many=True)
        return Response(serialize.data)


@api_view(['GET'])
def show_restaurants(request1, request2, request3, request4):
    if request1.method == 'GET':
        # query_set = 0
        open_restaurants = RestTimingss.objects.filter(day_num=request2) & RestTimingss.objects.filter(opening_time__lte=request3) & RestTimingss.objects.filter(closing_time__gte=request3)
        rest_det = RestaurantDetail.objects.filter(restaurant_id__in=open_restaurants.values('restaurant'))
        # serialize3 = searialize_rest_timingss(open_restaurants, many=True)
        serialize2 = searialize_rest_detail(rest_det, many=True)
        # final_serialize = searialize_rest_detail(serialize2.data, many=True)
        # print(type(serialize2))
        # temp = []
        #
        # for it in open_restaurants:
        #     temp.append(it.restaurant.restaurant_name)
            # temp.append(searialize_rest_timingss(it.restaurant.restaurant_name, many=True))
        # print(type(open_restaurants))
        # print(str(open_restaurants.query))
        # pprint(open_restaurants.__dict__)
        # print(open_restaurants)
        return Response(serialize2.data)
        # return Response(temp.data)
        # return Response(json.dumps(json.JSONDecoder().decode(temp)))
        # return Response(rest_det.values('restaurant_name'))


@api_view(['GET'])
def show_top_restaurants1(request1, request2, request3, request4, request5, request6, request7):
    # print(request1)
    # print(request2)  #y
    # print(request3)  #x
    # print(request4)  #start
    # print(request5)
    # print(request6)  #end
    # print(request7)
    # return HttpResponse("Show top restaurants page!!!!")

    if request1.method == 'GET':
        menu_object = (MenuDetails.objects.filter(menu_price__gte=request4) & MenuDetails.objects.filter(menu_price__lte=request6)).values('restaurant').annotate(total=Count('dish_name')).filter(total__gt=request3)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by('-cash_balance')[:int(request2)]
        ser = searialize_rest_detail(rest_det, many=True)
        # menu_object = MenuDetails.objects.filter(menu_price__gte=request4) & MenuDetails.objects.filter(menu_price__lte=request6)
        # print(menu_object)
        # serialize = searialize_menu_details(menu_object, many=True)
        # return Response(serialize.data)
        # print(type(menu_object.values('restaurant')))
        # return Response(menu_object)
        # return Response(menu_object.values('restaurant'))
        # return HttpResponse("Show top restaurants page!!!!")
        return Response(ser.data)
        # return Response(rest_det.values('restaurant_name'))


@api_view(['GET'])
def show_top_restaurants2(request1, request2, request3, request4, request5, request6, request7):

    if request1.method == 'GET':
        menu_object = (MenuDetails.objects.filter(menu_price__gte=request4) & MenuDetails.objects.filter(menu_price__lte=request6)).values('restaurant').annotate(total=Count('dish_name')).filter(total__lt=request3)
        rest_det = (RestaurantDetail.objects.filter(restaurant_id__in=menu_object.values('restaurant'))).order_by('-cash_balance')[:int(request2)]
        return Response(rest_det.values('restaurant_name'))

