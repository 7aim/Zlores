from django.urls import path 
from . import views

urlpatterns = [
    path('myposts', views.myposts_request, name='myposts'),
    path('postdetail/<int:id>/', views.post_detail_request, name='postdetail'),
    
    path('createpost', views.createpost_request, name='createpost'),
    path('deletepost/<int:id>/', views.deletepost_request, name='deletepost'),
    path('updatepost/<int:id>/', views.updatepost_request, name='updatepost'),
    
    path('deletecomment/<int:postid>/<int:commentid>/', views.deletecomment_request, name='deletecomment'),
    path('addcomment/<int:id>/', views.addcomment_request, name='addcomment'),
]
