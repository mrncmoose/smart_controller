from django.db import models
from django.template.defaultfilters import default


class Customer(models.Model):
    #Note:  The customer is assumed to be a partner in IRS terms.
    name = models.CharField(max_length=255, default='')
    ein = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    postal_code = models.CharField(max_length=255, default='')

class Account(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    isActive = models.BooleanField
    openDate = models.DateField
    closeDate = models.DateField

class EventType(models.Model):
    description = models.CharField(max_length=255)
    shortDescription = models.CharField(max_length=255)
    

class Event(models.Model):
    amount = models.FloatField
    isActive = models.BooleanField
    creditType = models.CharField(max_length=255)
    updateSquence = models.IntegerField
    fundingSquence = models.IntegerField
    eventType = EventType
      
class Projection(models.Model):
    amount = models.FloatField
    investmentDate = models.DateField
    approvalStatus = models.CharField(max_length=255)
    projectionDate = models.DateField
    amount = models.FloatField
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)

class InvestmentStatus(models.Model):
    status = models.CharField(max_length=255)
   
class Investment(models.Model):   
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255)
    portfolio = models.CharField(max_length=255)
    investmentClass = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    dispositionDate = models.DateField
    dryClosingDate = models.DateField
    closingDate = models.DateField
    updatedTimestamp = models.DateTimeField
    accountingMethod = models.CharField(max_length=255) # Enumerated
    taxRate = models.FloatField
    staticTaxRate = models.FloatField
    status = models.ForeignKey(InvestmentStatus, on_delete=models.CASCADE, default=None)
    status = InvestmentStatus
    projection = models.ForeignKey(Projection, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)

class InvestmentOriginator(models.Model):
    name = models.CharField(max_length=255, default='')
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, default=None)

class JournalEntry(models.Model):
    #account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account = Account
    entry_date = models.DateField
    amount = models.FloatField
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, default=None)
    