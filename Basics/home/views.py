from django.shortcuts import render, HttpResponse
from .models import CustomerDetails
from .serialization import searialization_class, searialization_class1, searialization_class2
from .models import CustomerDetails, RestaurantDetail, RestTimingss
from rest_framework.response import Response
from rest_framework.decorators import api_view


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


# def show_restaurants(request1, request2, request3, request4):
#     print(request1)
#     print(request2)
#     print(request3)
#     print(request4)
#     return HttpResponse("This is show restaurants!!!!!!")

@api_view(['GET'])
def show_restaurants(request1, request2, request3, request4):
    if request1.method == 'GET':
        open_restaurants = RestTimingss.objects.filter(day_num=request2) & RestTimingss.objects.filter(opening_time__lte=request3) & RestTimingss.objects.filter(closing_time__gte=request3)
        serialize2 = searialization_class2(open_restaurants, many=True)
        return Response(serialize2.data)

# /([0-6])/(([01]\d|2[0-3]):[0-5]\d)


# def display_data(request):
#     call_api = 0
#     return render(request, 'contacts.html')
