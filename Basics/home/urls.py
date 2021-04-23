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
    # path("show_restaurants", v1.show_restaurants, name='show_restaurants')
    re_path(r'^show_restaurants/([0-6])/(([01]\d|2[0-3]):?[0-5]\d)', v1.show_restaurants, name='show_restaurants'),
    re_path(r'^show_top_restaurants/y=([0-9]+)/x=([0-9]+)/price_range=([0-9]+(\.[0-9]{1,2}))-([0-9]+(\.[0-9]{1,2}))', v1.show_top_restaurants, name='show_restaurants')
]
