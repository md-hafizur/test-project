from django.urls import path, include
from account.views import UserRegistrationView, login, UserDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', login.as_view(), name='user-login'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),

]