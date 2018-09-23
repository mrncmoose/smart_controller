'''
Created on Sep 16, 2018

@author: fdunaway
'''
from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
# from .views import CreateView

app_name = 'amortization'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]

#TODO: Correctly add REST API's
# apiUrlPatterns = [
#     url(r'^customerlists/$', CreateView.as_view(), name="create"),
# ]
# urlpatterns = format_suffix_patterns(apiUrlPatterns)
