from django.urls import path, re_path
from . import views


urlpatterns = [
    path('quizzes', views.QuizListAPI.as_view()),
    re_path(r'quizess/(?P<slug>[\w\-]+)/$', views.QuizDetailAPI.as_view()),
]