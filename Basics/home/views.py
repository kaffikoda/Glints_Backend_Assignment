from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("This is the home page!!!!!")


def about(request):
    return HttpResponse("This is the about page!!!!!")


def services(request):
    return HttpResponse("This is the services page!!!!!")


def contacts(request):
    return HttpResponse("This is contacts page!!!!!!!!!")
