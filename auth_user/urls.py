from django.urls import path
from .views import LoginView, RegisterView, TokenRefreshViewCustom


urlpatterns = [
    path('auth', LoginView.as_view(), name='login'),
    path('refresh', TokenRefreshViewCustom.as_view(), name='refresh'),
    path('register', RegisterView.as_view(), name='register'),
]
