from django.test import TestCase
# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,  
    TokenVerifyView,
)

from .views import MedicineViewSet, BillViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'bills', BillViewSet, basename='bill')
urlpatterns = router.urls