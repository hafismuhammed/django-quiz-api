from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('user/', views.UserAPI.as_view()),
]