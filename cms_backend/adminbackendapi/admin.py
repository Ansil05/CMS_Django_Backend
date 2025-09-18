from django.contrib import admin

# Register your models here.
from adminbackendapi.models import Role, Staff, Doctor, Specialization

admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Doctor)
admin.site.register(Specialization)