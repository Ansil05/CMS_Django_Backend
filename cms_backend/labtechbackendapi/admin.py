from django.contrib import admin

from .models import Labrecord,Labtest
# Register your models here.
admin.site.register(Labtest)
admin.site.register(Labrecord)
