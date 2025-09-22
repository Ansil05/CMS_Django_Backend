from django.urls import path
from .views import LabtestListCreate, LabtestRetrieveUpdateDestroy, LabrecordListCreate, LabrecordRetrieveUpdateDestroy
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'labtests', LabtestListCreate, basename='labtest')
router.register(r'labrecords', LabrecordListCreate, basename='labrecord')
urlpatterns = router.urls
