from django.shortcuts import render, HttpResponse
from .models import CustomerDetails
from .serialization import searialization_class, searialize_rest_detail, searialize_rest_timingss
from .models import CustomerDetails, RestaurantDetail, RestTimingss
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
        open_restaurants = (RestTimingss.objects.filter(day_num=request2) & RestTimingss.objects.filter(opening_time__lte=request3) & RestTimingss.objects.filter(closing_time__gte=request3)).prefetch_related('restaurant')
        # serialize2 = searialize_rest_detail(searialize_rest_timingss(open_restaurants, many=True), many=True)
        serialize2 = searialize_rest_timingss(open_restaurants, many=True)
        # final_serialize = searialize_rest_detail(serialize2.data, many=True)
        # print(type(serialize2))
        temp = []

        for it in open_restaurants:
            temp.append(it.restaurant.restaurant_name)
            # temp.append(searialize_rest_timingss(it.restaurant.restaurant_name, many=True))
        # print(type(open_restaurants))
        # print(str(open_restaurants.query))
        # pprint(open_restaurants.__dict__)
        # print(open_restaurants)
        return Response(serialize2.data)
        # return Response(temp.data)
        # return Response(json.dumps(json.JSONDecoder().decode(temp)))



# /([0-6])/(([01]\d|2[0-3]):[0-5]\d)


# def display_data(request):
#     call_api = 0
#     return render(request, 'contacts.html')
