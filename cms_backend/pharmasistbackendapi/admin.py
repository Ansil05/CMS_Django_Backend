from django.contrib import admin
from .models import Medicine, Bill

admin.site.register(Medicine)
admin.site.register(Bill)