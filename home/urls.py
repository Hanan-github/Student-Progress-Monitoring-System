from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('contact/', views.contact, name='contact'),


    path('test/', views.test, name='test'),
    path('testb/', views.testb, name='testb'),

    #for 404 page
    path('404-not-found', views.notfound, name='notfound'),

]