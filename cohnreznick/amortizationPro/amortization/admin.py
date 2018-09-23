from django.contrib import admin

from .models import Customer, Account, JournalEntry, Projection, Investment, InvestmentStatus

# Register your models here.
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(JournalEntry)
admin.site.register(Projection)
admin.site.register(Investment)
admin.site.register(InvestmentStatus)
