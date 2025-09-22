from django.urls import path
from .views import (
    LabtestListCreateView, LabtestDetailView,
    LabrecordListCreateView, LabrecordDetailView
)

urlpatterns = [
    path('labtests/', LabtestListCreateView.as_view(), name='labtest-list-create'),
    path('labtests/<int:pk>/', LabtestDetailView.as_view(), name='labtest-detail'),
    path('labrecords/', LabrecordListCreateView.as_view(), name='labrecord-list-create'),
    path('labrecords/<int:pk>/', LabrecordDetailView.as_view(), name='labrecord-detail'),
]
