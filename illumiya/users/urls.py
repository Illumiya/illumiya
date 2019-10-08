from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'register/',
         CustomRegitrationView.as_view(),
         name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]