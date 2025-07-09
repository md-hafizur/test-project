from django.urls import path, include
from account.views import UserRegistrationView, login

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', login.as_view(), name='user-login'),
]