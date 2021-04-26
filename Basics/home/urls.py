"""Basics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from home import views as view1

urlpatterns = [
    path("", view1.index, name='home'),
    path("about", view1.about, name='about'),
    path("services", view1.services, name='services'),
    path("contacts", view1.contacts, name='contacts'),
    # path("show", view1.show_customer_details, name='show_customer'),
    path("restaurants", view1.restaurants, name='show_restaurants'),
    path("relevant_restaurants", view1.relevant_restaurants, name="relevant_restaurants"),
    path("relevant_dishes", view1.relevant_dishes, name="relevant_dishes"),
    path("place_order", view1.place_order, name='place_order')
]
