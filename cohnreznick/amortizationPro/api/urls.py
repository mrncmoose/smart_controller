'''
Created on Sep 23, 2018

@author: moose
'''
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'customers/$', views.customer_list),
    url(r'customer/(?P<pk>[0-9]+)/$', views.customer_detail),
]