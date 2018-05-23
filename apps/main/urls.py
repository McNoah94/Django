from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'validate/', views.validate), #Validates registration info and makes flash messages
    url(r'login/', views.login), #Validates login info and makes flash messages
    url(r'travels/$', views.travels),#Dashboard
    url(r'travels/add/', views.add),
    url(r'logout/', views.logout),#Logs out, clears session data
    url(r'newplan/', views.newPlan),
    url(r'travels/destination/(?P<x>\d+)/', views.showTrip),#Shows trip information
    url(r'join/(?P<x>\d+)/', views.join),#Allows user to join a trip
]