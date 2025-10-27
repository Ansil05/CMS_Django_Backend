from django.urls import path
from .views import SignUpAPIView,LoginAPIView,GroupList,DeleteUserByEmailAPIView,CheckUsernameAPIView,CheckEmailAPIView
from rest_framework_simplejwt.views import TokenRefreshView
 
urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('roles/', GroupList.as_view(), name='group_list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', DeleteUserByEmailAPIView.as_view(), name='delete_user'),
    path('check-username/', CheckUsernameAPIView.as_view(), name='check_username'),
    path('check-email/', CheckEmailAPIView.as_view(), name='check_email'),
]