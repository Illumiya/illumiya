from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('contact-us/', views.ContactView.as_view(), name='contact-us'),
    path('create/comment/', views.CreateCommentView.as_view(), name='create-comment'),
    path('sub-comment/<int:pk>/', views.AjaxCommentDetailView.as_view(), name='sub-comment-detail'),
    path('main-comment/<int:object_pk>/', views.AjaxCommentDetailView.as_view(), name='main-comment-detail'),
]