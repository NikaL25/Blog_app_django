from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('create/', views.create_blog, name='create_blog'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('<int:pk>/update/', views.update_blog, name='update_blog'),
    path('<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    path('<int:pk>/like/', views.like_blog, name='like_blog'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/update/', views.update_comment, name='update_comment'),
]