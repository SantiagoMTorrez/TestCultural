from django.urls import path
from .views import (
    TestCreationView,
    QuestionRetrieveView,
    AnswerSubmissionView,
    CategoryCreateView,
    CategoryListView,
    QuestionCreationView,
    QuestionEditView,
    QuestionListView,
    TestResultView,
    QuestionTypeView
)

urlpatterns = [
    path('tests/create/', TestCreationView.as_view(), name='test-create'),
    path('tests/<int:participation_id>/question/<int:question_number>/', QuestionRetrieveView.as_view(), name='question-retrieve'),
    path('tests/<int:participation_id>/question/<int:question_number>/answer/', AnswerSubmissionView.as_view(), name='answer-submission'),
    path('tests/<int:participation_id>/result/', TestResultView.as_view(), name='test-result'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('questions/create/', QuestionCreationView.as_view(), name='question-create'),
    path('questions/<int:pk>/edit/', QuestionEditView.as_view(), name='question-edit'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('question-types/', QuestionTypeView.as_view({'get': 'list',
                                                        'post': 'create',
                                                        'put': 'update', 'delete': 'destroy'}), name='question-type-list'),
]
