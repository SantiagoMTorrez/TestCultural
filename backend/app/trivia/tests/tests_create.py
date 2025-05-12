from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import status
from ..models import (
    Category, Question, AnswerOption, QuestionType, Test, TestParticipation,
    TestQuestion, ParticipationResponse
)

User = get_user_model()

class BaseAPITest(APITestCase):
    def setUp(self):

        self.admin_data = {
            'email' : 'admin1@example.com',
            'name': 'admin1',
            'password': 'password1234',
            'is_staff': True, 
        }

        self.user_data = {
            'email' : 'user@example.com',
            'name': 'user',
            'password': 'password1234',
            'is_staff': False, 
        }
        
        self.normal_user = get_user_model().objects.create_user(**self.user_data)
        self.admin_user = get_user_model().objects.create_user(**self.admin_data) 
        # Se generan tokens para cada usuario.
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION="Token " + self.normal_token.key)
        # Se crea un tipo de pregunta.
        self.qtype = QuestionType.objects.create(
            name="Multiple Choice", description="Multiple choice question"
        )
        # Se crea una categoría.
        self.category = Category.objects.create(
            name="General", description="General Knowledge"
        )
        # Se crean dos preguntas con sus opciones.
        self.question1 = Question.objects.create(
            created_by = self.admin_user,
            text="What is 2+2?",
            difficulty=1,
            explanation="2+2 is 4",
            score=5,
            category=self.category,
            question_type=self.qtype
        )
        AnswerOption.objects.create(question=self.question1, text="4", correct=True)
        AnswerOption.objects.create(question=self.question1, text="22", correct=False)
        self.question2 = Question.objects.create(
            created_by = self.admin_user,
            text="What is the capital of Spain?",
            difficulty=2,
            explanation="Madrid is the capital of Spain",
            score=10,
            category=self.category,
            question_type=self.qtype
        )
        AnswerOption.objects.create(question=self.question2, text="Madrid", correct=True)
        AnswerOption.objects.create(question=self.question2, text="Barcelona", correct=False)

class CategoryCreationTests(BaseAPITest):
    def test_admin_can_create_category(self):
        url = "/trivia/categories/"
        data = {"name": "Math", "description": "Questions about math"}
        response = self.client_admin.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Math")

    def test_non_admin_cannot_create_category(self):
        url = "/trivia/categories/"
        data = {"name": "Science", "description": "Questions about science"}
        response = self.client_user.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class QuestionCreationTests(BaseAPITest):
    def test_admin_can_create_question(self):
        url = "/trivia/questions/create/"
        data = {
            "text": "What is the color of the sky?",
            "difficulty": 1,
            "explanation": "The sky is blue.",
            "score": 5,
            "category": self.category.id,
            "question_type": self.qtype.id,
            "answer_options": [
                {"text": "Blue", "correct": True},
                {"text": "Green", "correct": False},
                {"text": "Red", "correct": False}
            ]
        }
        response = self.client_admin.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "What is the color of the sky?")
        self.assertEqual(len(response.data["answer_options"]), 3)

    def test_non_admin_cannot_create_question(self):
        url = "/trivia/questions/create/"
        data = {
            "text": "What is 3+3?",
            "difficulty": 1,
            "explanation": "3+3 is 6.",
            "score": 5,
            "category": self.category.id,
            "question_type": self.qtype.id,
            "answer_options": [
                {"text": "6", "correct": True},
                {"text": "8", "correct": False}
            ]
        }
        response = self.client_user.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestCreationAndParticipationTests(BaseAPITest):
    def create_test(self, n, category=None):
        url = "/trivia/tests/create/"
        data = {"n": n}
        if category:
            data["category"] = category
        return self.client_user.post(url, data, format="json")

    def test_create_test_successfully(self):
        response = self.create_test(2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("test_id", response.data)
        self.assertIn("participation_id", response.data)
        self.assertEqual(response.data["total_questions"], 2)

    def test_create_test_insufficient_questions(self):
        response = self.create_test(10, category=self.category.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class QuestionRetrieveAndAnswerTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        create_url = "/trivia/tests/create/"
        test_response = self.client_user.post(create_url, {"n": 2}, format="json")
        self.participation_id = test_response.data["participation_id"]

    def test_submit_same_question_twice(self):
        url_answer = f"/trivia/tests/{self.participation_id}/question/1/answer/"
        url_question = f"/trivia/tests/{self.participation_id}/question/1/start/"
        question_response = self.client_user.get(url_question, format="json")
        option_id = question_response.data["answer_options"][0]["id"]
        answer_data = {"answer_option": option_id}
        response_first = self.client_user.post(url_answer, answer_data, format="json")
        self.assertEqual(response_first.status_code, status.HTTP_200_OK)
        response_duplicate = self.client_user.post(url_answer, answer_data, format="json")
        self.assertEqual(response_duplicate.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_question(self):
        url = f"/trivia/tests/{self.participation_id}/question/1/"
        response = self.client_user.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text", response.data)
        self.assertIn("answer_options", response.data)
        self.assertNotIn("explanation", response.data)

    def test_submit_answer_correctly_and_get_final_result(self):
        url_answer1 = f"/trivia/tests/{self.participation_id}/question/1/answer/"
        url_question1 = f"/trivia/tests/{self.participation_id}/question/1/start/"
        question_response = self.client_user.get(url_question1, format="json")
        correct_option_id = None
        if question_response.data["text"] == "What is 2+2?":
            for option in question_response.data["answer_options"]:
                if option["text"] == "4":
                    correct_option_id = option["id"]
        elif question_response.data["text"] == "What is the capital of Spain?":
            for option in question_response.data["answer_options"]:
                if option["text"] == "Madrid":
                    correct_option_id = option["id"]
        if not correct_option_id:
            correct_option_id = question_response.data["answer_options"][0]["id"]
        answer_data1 = {"answer_option": correct_option_id}
        response1 = self.client_user.post(url_answer1, answer_data1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertIn("is_correct", response1.data)
        self.assertIn("explanation", response1.data)
        url_answer2 = f"/trivia/tests/{self.participation_id}/question/2/answer/"
        url_question2 = f"/trivia/tests/{self.participation_id}/question/2/start/"
        question_response2 = self.client_user.get(url_question2, format="json")
        correct_option_id2 = None
        if question_response2.data["text"] == "What is 2+2?":
            for option in question_response2.data["answer_options"]:
                if option["text"] == "4":
                    correct_option_id2 = option["id"]
        elif question_response2.data["text"] == "What is the capital of Spain?":
            for option in question_response2.data["answer_options"]:
                if option["text"] == "Madrid":
                    correct_option_id2 = option["id"]
        if not correct_option_id2:
            correct_option_id2 = question_response2.data["answer_options"][0]["id"]
        answer_data2 = {"answer_option": correct_option_id2}
        response2 = self.client_user.post(url_answer2, answer_data2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertIn("final_result", response2.data)

class CategoryDeletionTests(BaseAPITest):
    def test_admin_puede_eliminar_categoria(self):
        url = f'/trivia/categories/{self.category.id}/'
        resp = self.client_admin.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_usuario_normal_no_puede_eliminar_categoria(self):
        url = f'/trivia/categories/{self.category.id}/'
        resp = self.client_user.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

class QuestionTypeDeletionTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.other_qtype = QuestionType.objects.create(
            name='TrueFalse', description='True or False'
        )

    def test_admin_puede_eliminar_tipo_pregunta(self):
        url = f'/trivia/question-types/{self.other_qtype.id}/'
        resp = self.client_admin.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(QuestionType.objects.filter(id=self.other_qtype.id).exists())

    def test_usuario_normal_no_puede_eliminar_tipo_pregunta(self):
        url = f'/trivia/question-types/{self.other_qtype.id}/'
        resp = self.client_user.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(QuestionType.objects.filter(id=self.other_qtype.id).exists())

class QuestionFilterTests(BaseAPITest):

    def test_filtrar_por_categoria(self):
        url = f'/trivia/questions/?category={self.category.id}'
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertEqual(item['category'], self.category.id)

    def test_filtrar_por_tipo(self):
        url = f'/trivia/questions/?question_type={self.qtype.id}'
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertEqual(item['question_type'], self.qtype.id)

    def test_filtrar_por_difficulty_min(self):
        url = '/trivia/questions/?difficulty_min=2'
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertGreaterEqual(item['difficulty'], 2)

    def test_filtrar_por_difficulty_max(self):
        url = '/trivia/questions/?difficulty_max=2'
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertLessEqual(item['difficulty'], 2)

    def test_filtrar_por_rango_completo(self):
        url = '/trivia/questions/?difficulty_min=1&difficulty_max=2'
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertTrue(1 <= item['difficulty'] <= 2)

    def test_filtrar_combinado(self):
        url = (
            f'/trivia/questions/?category={self.category.id}'
            f'&question_type={self.qtype.id}'
            '&difficulty_min=2'
        )
        resp = self.client_user.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['id'], self.question2.id)