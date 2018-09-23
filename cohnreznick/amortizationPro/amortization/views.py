from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from api.serializers import CustomerSerializer
from .models import Customer

from .models import Customer, Account, JournalEntry, Projection
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'amortizatoin/index.html'
    context_object_name = 'account_list'
    
class CustomerView(generic.ListView):
    model = Customer
    
class AccountView(generic.ListView):
    model = Account
    
class JournalEntryView(generic.ListView):
    model = JournalEntry
    
class Projection(generic.ListView):
    model = Projection

