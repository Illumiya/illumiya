from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('contact-us/', views.ContactView.as_view(), name='contact-us'),
    path('create/comment/', views.CreateCommentView.as_view(), name='create-comment'),
    #path('comment/detail/', views.ContactView.as_view(), name='contact-us'),
]