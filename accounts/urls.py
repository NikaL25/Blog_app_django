from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),

]
