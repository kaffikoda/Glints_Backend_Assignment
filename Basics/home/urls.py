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
from home import views as v1

urlpatterns = [
    path("", v1.index, name='home'),
    path("about", v1.about, name='about'),
    path("services", v1.services, name='services'),
    path("contacts", v1.contacts, name='contacts'),
    path("show", v1.show_customer_details, name='show_customer'),
    path("restaurants", v1.show_restaurants, name='show_restaurants'),
    path("top_restaurants", v1.top_restaurants, name='show_restaurants'),
    path("place_order", v1.place_order, name='place_order')
    # path("add_name", v1.add_name, name='add_name')
    # re_path("^show_restaurants?date=([0-6])&time=(([01]\d|2[0-3]):?[0-5]\d)", v1.show_restaurants, name="SR"),
    # re_path(r'^show_restaurants/([0-6])/(([01]\d|2[0-3]):?[0-5]\d)', v1.show_restaurants, name='show_restaurants'),
    # re_path(r'^show_top_restaurants/top=([0-9]+)/greater_than=([0-9]+)/price_range=([0-9]+(\.[0-9]{1,2}))-([0-9]+(\.[0-9]{1,2}))', v1.show_top_restaurants1, name='show_top_restaurants1'),
    # re_path(r'^show_top_restaurants/top=([0-9]+)/lesser_than=([0-9]+)/price_range=([0-9]+(\.[0-9]{1,2}))-([0-9]+(\.[0-9]{1,2}))', v1.show_top_restaurants2, name='show_top_restaurants2')
    # re_path(r'^place_order/user_id=((\d{1,}))/dish_name=(.*)/restaurant_name=(.*)', v1.dummy_function, name='dummy')
]
