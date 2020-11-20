from rest_framework import serializers
from .models import Quiz, Question, QuizTaker, Answer, UserAnswer


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'discription', 'image', 'slug', 'questions_count']
        read_only_field = ['questions_count', ]

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'label']

class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


class QuizTakerSerializer(serializers.ModelSerializer):
    useranswer_set = UserAnswerSerializer(many=True)

    class Meta:
        model = QuizTaker
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    quiztakers_set = serializers.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiztakers_set(self, obj):
        try:
            quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            serializer = QuizTakerSerializer(quiz_taker)
            return serializer.data
        except QuizTaker.DoesNotExist:
            return None


class MyQuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'discription', 'image', 'slug', 'questions_count', 'completed', 'score', 'progress']
        read_only_field = ['questions_count', 'completed', 'score', 'progress']

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

    def get_completed(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            return quiztaker.completed
        except QuizTaker.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == False:
                questions_answered = UserAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count() 
                total_questions = obj.question_set.all().count()
                return int(questions_answered / total_questions)
            return None
        except QuizTaker.DoesNotExist:
            return None

    def get_score(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == True:
                return quiztaker.score
            return None
        except QuizTaker.DoesNotExist:
            return None
                