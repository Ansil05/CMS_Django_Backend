from django.contrib import admin

from .models import Labrecord,Labtest,LabTestRequest,LabBill
# Register your models here.
admin.site.register(Labtest)
admin.site.register(Labrecord)
admin.site.register(LabTestRequest)
admin.site.register(LabBill)
