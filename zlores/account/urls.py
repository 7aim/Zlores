from django.urls import path 
from . import views

urlpatterns = [
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('resetpassword', views.resetpassword_request, name='resetpassword'),
    path('profile', views.profile_request, name='profile'),
    path('userprofile/<str:author>/', views.userprofile_request, name='userprofile'),
    path('follow/<str:author>/', views.follow_request, name='follow'),
    path('unfollow/<str:author>/', views.unfollow_request, name='unfollow'),
]
