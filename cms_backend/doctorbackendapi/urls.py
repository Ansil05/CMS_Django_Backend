from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet, PrescriptionViewSet, LabPrescriptionViewSet

router = DefaultRouter()
router.register(r'consultations', ConsultationViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'lab-prescriptions', LabPrescriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]