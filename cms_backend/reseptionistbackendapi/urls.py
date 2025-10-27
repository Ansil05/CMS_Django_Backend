from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AppointmentViewSet, ReceptionBillViewSet


router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'bills', ReceptionBillViewSet)

urlpatterns = router.urls