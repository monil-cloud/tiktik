"""tiktik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from admin_api import views

urlpatterns = [
    path('adminUserAdd' , views.AdminUserAdd.as_view(), name="AdminUser"),
    path('CheckUserData', views.CheckUserData.as_view(), name="checkUserData"),
    path('personalDetail', views.PersonDetail.as_view(), name='personaldetail'),
    path('UserDetail', views.UserDetail.as_view(), name="userDetail"),
    #category API
    path('adminCategory', views.AdminCategory.as_view(), name="adminCategory"),
    #banner API
    path('banner', views.BannerDetail.as_view(), name='bannerDetail')
]
