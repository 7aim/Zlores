from django.urls import path 
from . import views

urlpatterns = [
    path('createpost', views.createpost_request, name='createpost'),
]
