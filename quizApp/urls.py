from django.urls import path
from . import views


urlpatterns = [
    path('quizzes/', views.QuizListAPI.as_view()),
    path('quizzes/<slug:slug>/', views.QuizDetailAPI.as_view()),
    path('my-quizzes/', views.MyQuizAPIView.as_view()),
    path('save-answer/', views.SaveUsersAnswer.as_view()),
    path('quizzes/<slug:slug>/submit/', views.SubmitQuizAPI.as_view()),
]