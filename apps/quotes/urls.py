from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.main),
    url(r'quotes/', views.main),
    url(r'login/', views.login),
    url(r'validate/', views.validate),
    url(r'dashboard/', views.dashboard),
    url(r'addQuote/', views.addQuote),
    url(r'addFav/(?P<x>\d+)/', views.addFav),
    url(r'remFav/(?P<x>\d+)/', views.remFav),
    url(r'clear/', views.clear),
    url(r'users/(?P<x>\d+)/', views.user),
]