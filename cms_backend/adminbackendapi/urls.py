from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, SpecializationViewSet, StaffViewSet, DoctorViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'staffs', StaffViewSet)
router.register(r'doctors', DoctorViewSet)

urlpatterns = router.urls
