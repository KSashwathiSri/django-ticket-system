from django.contrib import admin
# Register your models here.
from .models import Customer,Agent,Tickets
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(Tickets)