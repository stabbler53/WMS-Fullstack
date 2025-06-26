from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Inbound, Outbound

admin.site.register(Inbound)
admin.site.register(Outbound)
