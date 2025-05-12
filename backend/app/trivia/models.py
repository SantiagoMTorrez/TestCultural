from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class QuestionType(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    multiplayer = models.BooleanField(default=False)
    time_limit_minutes = models.IntegerField(default=60)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    difficulty = models.IntegerField()
    explanation = models.TextField(blank=True)
    score = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    # answer_options = models.

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_question')
    question_number = models.IntegerField()

    def __str__(self):
        return f"Test {self.test.id} - Question {self.question_number}"


class TestParticipation(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participation by {self.user} in {self.test.title}"


class ParticipationResponse(models.Model):
    test_participation = models.ForeignKey(TestParticipation, on_delete=models.CASCADE)
    test_question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Response for Participation {self.test_participation.id} on TestQuestion {self.test_question.id}"
