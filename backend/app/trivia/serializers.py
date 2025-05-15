from rest_framework import serializers
from .models import (
    Test, TestQuestion, TestParticipation, Question, AnswerOption, ParticipationResponse,
    Category, QuestionType
)
from rest_framework.serializers import PrimaryKeyRelatedField

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'

class AnswerOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'text', 'correct')

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'text')

class QuestionStatementSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id', 'text', 'score', 'difficulty', 'answer_options')

class QuestionResultSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionCreateSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id', 'text', 'score', 'difficulty', 'answer_options', 'explanation')

class TestCreationSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1)
    category = serializers.IntegerField(required=False, allow_null=True)
    time_limit_minutes = serializers.IntegerField(required=False)

class TestCreationResponseSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    participation_id = serializers.IntegerField()
    total_questions = serializers.IntegerField()

class AnswerSubmissionSerializer(serializers.Serializer):
    answer_option = serializers.IntegerField()

class AnswerSubmissionResponseSerializer(serializers.Serializer):
    is_correct    = serializers.BooleanField()
    explanation   = serializers.CharField()
    earned_score  = serializers.FloatField()
    final_result  = serializers.DictField(required=False)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class QuestionCreateSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionCreateSerializer(many=True)
    created_by = PrimaryKeyRelatedField(read_only=True, required=False)
    class Meta:
        model = Question
        fields = ('id', 'text', 'difficulty', 'explanation', 'score', 'category', 'question_type', 'answer_options', 'created_by')
    def create(self, validated_data):
        options_data = validated_data.pop('answer_options')
        question = Question.objects.create(**validated_data)
        for option in options_data:
            AnswerOption.objects.create(question=question, **option)
        return question
