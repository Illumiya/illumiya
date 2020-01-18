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
    path('videos/', views.VideoListView.as_view(), name='video-list'),
    path('my-videos/', views.MyVideosView.as_view(), name='my-videos'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('blog/manage-like/<int:blog_id>/', views.BlogManageLikeView.as_view(), name='blog-manage-like'),
    path('payment/order/', views.PayOrderView.as_view(), name='pay-order'),
    path('payment/status/', views.PaymentStatusView.as_view(), name='payment-status'),
]