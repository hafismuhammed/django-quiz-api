from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from .models import Question, Quiz, QuizTaker, Answer, UserAnswer
from .serializers import QuizSerializer, QuizDetailSerializer, QuestionSerializer, AnswerSerializer, UserAnswerSerializer, QuizTakerSerializer


class QuizListAPI(generics.ListAPIView):
    #queryset = Quiz.objects.filter(rollout=True)
    serializer_class = QuizSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter(rollout=True)
        #queryset = Quiz.objects.filter(rollout=True).exclude(quiztaker__user=self.request.user)
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(discription__icontains=query)                
            ).distinct()

        return queryset

class QuizDetailAPI(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    #permission_classes = []

    def get(self, *args, **kwargs):
        slug = self.kwargs['slug']
        quiz = get_object_or_404(Quiz, slug=slug)
        last_question = None
        obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)

        if created:
            for question in Question.objects.filter(quiz=quiz):
                UserAnswer.objects.create(quiz_taker=obj, question=question)
        else:
            last_question = UserAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
            if last_question.count() > 0:
                last_question = last_question.last().question.id
            else:
                last_question = None
        
        return Response({
            'quiz': self.get_serializer(quiz, context={'request': self.request}).data, 
            'last_question': last_question,
            })

