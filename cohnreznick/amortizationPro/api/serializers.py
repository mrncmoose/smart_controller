'''
Created on Sep 20, 2018

@author: fdunaway
'''
from rest_framework import serializers
from amortization.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('name', 'ein', 'address', 'state', 'postal_code')