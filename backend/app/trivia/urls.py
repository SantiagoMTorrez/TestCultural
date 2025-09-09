from django.urls import path, include
from .views import (
    TestCreationView,
    QuestionRetrieveView,
    AnswerSubmissionView,
    CategoryViewSet,
    QuestionCreationView,
    QuestionEditView,
    QuestionListView,
    QuestionDeleteView,
    TestResultView,
    QuestionTypeView,
    QuestionRetrieveAndAccessView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'question-types', QuestionTypeView, basename='question-type')

urlpatterns = [
    path('tests/create/', TestCreationView.as_view(), name='test-create'),
    path('tests/<int:participation_id>/question/<int:question_number>/', QuestionRetrieveView.as_view(), name='question-retrieve'),
    path('tests/<int:participation_id>/question/<int:question_number>/start/', QuestionRetrieveAndAccessView.as_view(), name='question-retrieve-and-access'),
    path('tests/<int:participation_id>/question/<int:question_number>/answer/', AnswerSubmissionView.as_view(), name='answer-submission'),
    path('tests/<int:participation_id>/result/', TestResultView.as_view(), name='test-result'),
    path('questions/create/', QuestionCreationView.as_view(), name='question-create'),
    path('questions/<int:pk>/edit/', QuestionEditView.as_view(), name='question-edit'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('', include(router.urls))
]
