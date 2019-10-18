from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail')
]