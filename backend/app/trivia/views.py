import random
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import (
    Test, TestQuestion, TestParticipation, Question, AnswerOption, ParticipationResponse, 
    Category, QuestionType
)
from core.permissions import IsAdminOrReadOnly
from .serializers import (
    TestCreationSerializer,
    TestCreationResponseSerializer,
    QuestionStatementSerializer,
    AnswerSubmissionSerializer,
    AnswerSubmissionResponseSerializer,
    CategorySerializer,
    QuestionCreateSerializer,
    QuestionTypeSerializer
)
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    summary="Creación de test",
    description="Crea un test con n preguntas aleatorias. Si se especifica un ID de categoría, se seleccionan preguntas de esa categoría.",
    request=TestCreationSerializer,
    responses={201: TestCreationResponseSerializer, 400: OpenApiTypes.OBJECT},
    tags=["Tests"],
    examples=[OpenApiExample('Ejemplo de creación de test', value={'n': 5, 'category': 2, 'time_limit_minutes': 10}, request_only=True)]
)
class TestCreationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TestCreationSerializer(data={**request.data})
        if serializer.is_valid():
            n = serializer.validated_data['n']
            category_id = serializer.validated_data.get('category')
            if category_id:
                questions = list(Question.objects.filter(category__id=category_id))
            else:
                questions = list(Question.objects.all())
            if len(questions) < n:
                return Response({"error": "No existen suficientes preguntas que cumplan con los requisitos."}, status=status.HTTP_400_BAD_REQUEST)
            selected_questions = random.sample(questions, n)
            with transaction.atomic():
                test = Test.objects.create(title=f"Test para {request.user}", multiplayer=False)
                participation = TestParticipation.objects.create(score=0, user=request.user, test=test)
                for index, question in enumerate(selected_questions, start=1):
                    TestQuestion.objects.create(test=test, question=question, question_number=index)
            response_data = {"test_id": test.id, "participation_id": participation.id, "total_questions": n}
            response_serializer = TestCreationResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Recuperar enunciado de pregunta",
    description="Devuelve el enunciado y las opciones de respuesta de una pregunta específica de un test.",
    # parameters=[
    #     OpenApiParameter("participation_id", OpenApiTypes.INT, description="ID de la participación", required=True),
    #     OpenApiParameter("question_number", OpenApiTypes.INT, description="Número secuencial de la pregunta", required=True)
    # ],
    responses={200: QuestionStatementSerializer, 404: OpenApiTypes.OBJECT},
    tags=["Tests"]
)
class QuestionRetrieveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, participation_id, question_number):
        try:
            participation = TestParticipation.objects.get(id=participation_id, user=request.user)
        except TestParticipation.DoesNotExist:
            return Response({"error": "Participación no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        try:
            test_question = TestQuestion.objects.get(test=participation.test, question_number=question_number)
        except TestQuestion.DoesNotExist:
            return Response({"error": "Pregunta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        question = test_question.question
        question_serializer = QuestionStatementSerializer(question)
        return Response(question_serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Envío de respuesta",
    description="Recibe la respuesta de una pregunta, indica si es correcta y devuelve la explicación. Si es la última pregunta, incluye el resultado final del test.",
    # parameters=[
    #     OpenApiParameter("participation_id", OpenApiTypes.INT, description="ID de la participación", required=True),
    #     OpenApiParameter("question_number", OpenApiTypes.INT, description="Número secuencial de la pregunta", required=True)
    # ],
    request=AnswerSubmissionSerializer,
    responses={200: AnswerSubmissionResponseSerializer, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
    tags=["Tests"],
    examples=[OpenApiExample('Ejemplo de envío de respuesta', value={'answer_option': 3}, request_only=True)]
)
class AnswerSubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, participation_id, question_number):
        try:
            participation = TestParticipation.objects.get(id=participation_id, user=request.user)
        except TestParticipation.DoesNotExist:
            return Response({"error": "Participación no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()
        time_limit = participation.test.time_limit_minutes
        end_time = participation.started_at + timezone.timedelta(minutes=time_limit)
        if current_time > end_time:
            return Response({"error": "Se ha excedido el límite de tiempo del test."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            test_question = TestQuestion.objects.get(test=participation.test, question_number=question_number)
        except TestQuestion.DoesNotExist:
            return Response({"error": "Pregunta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        if ParticipationResponse.objects.filter(test_participation=participation, test_question=test_question).exists():
            return Response({"error": "Esta pregunta ya fue contestada."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AnswerSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        answer_option_id = serializer.validated_data['answer_option']
        try:
            answer_option = AnswerOption.objects.get(id=answer_option_id, question=test_question.question)
        except AnswerOption.DoesNotExist:
            return Response({"error": "Opción de respuesta inválida para esta pregunta."}, status=status.HTTP_400_BAD_REQUEST)
        
        is_correct = answer_option.correct
        explanation = test_question.question.explanation
        
        with transaction.atomic():
            ParticipationResponse.objects.create(
                test_participation=participation,
                test_question=test_question,
                answer_option=answer_option
            )
            if is_correct:
                participation.score += test_question.question.score
                participation.save()
        
        response_data = {"is_correct": is_correct, "explanation": explanation}
        total_questions = TestQuestion.objects.filter(test=participation.test).count()
        
        if test_question.question_number == total_questions:
            responses = ParticipationResponse.objects.filter(test_participation=participation)
            correct_count = sum(1 for resp in responses if resp.answer_option.correct)
            final_result = {
                "total_score": participation.score,
                "correct_answers": correct_count,
                "total_questions": total_questions
            }
            response_data["final_result"] = final_result
        
        response_serializer = AnswerSubmissionResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(
    summary="Creación de categoría",
    description="Crea una nueva categoría. Sólo el administrador puede utilizar este endpoint.",
    request=CategorySerializer,
    responses={201: CategorySerializer, 400: OpenApiTypes.OBJECT},
    tags=["Categories"],
    examples=[OpenApiExample('Ejemplo de creación de categoría', value={'name': 'Matemáticas', 'description': 'Preguntas de matemáticas'}, request_only=True)]
)
class CategoryCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Listar categorías",
    description="Lista todas las categorías existentes.",
    responses={200: CategorySerializer(many=True)},
    tags=["Categories"]
)
class CategoryListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

@extend_schema(
    summary="Creación de pregunta",
    description="Crea una nueva pregunta con opciones de respuesta. Se espera un objeto JSON con los datos de la pregunta y una lista de opciones (texto y bandera 'correct'). Se asume que el usuario es administrador.",
    request=QuestionCreateSerializer,
    responses={201: QuestionCreateSerializer, 400: OpenApiTypes.OBJECT},
    tags=["Questions"],
    examples=[OpenApiExample('Ejemplo de creación de pregunta', 
                value={
                    'text': '¿Cuál es la capital de Francia?',
                    'difficulty': 2,
                    'explanation': 'París es la capital de Francia.',
                    'score': 10,
                    'category': 1,
                    'question_type': 1,
                    'answer_options': [
                        {'text': 'París', 'correct': True},
                        {'text': 'Marsella', 'correct': False},
                        {'text': 'Lyon', 'correct': False}
                    ]
                }, request_only=True)]
)
class QuestionCreationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = QuestionCreateSerializer(data={**request.data},
                                               context={'request': request})
        if serializer.is_valid():
            question = serializer.save(created_by = request.user)
            return Response(QuestionCreateSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Editar pregunta",
    description="Permite editar una pregunta creada por el usuario. Solo el creador (campo created_by) puede editar la pregunta.",
    request=QuestionCreateSerializer,
    responses={200: QuestionCreateSerializer, 400: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
    tags=["Questions"],
    examples=[OpenApiExample('Ejemplo de edición de pregunta', value={
                    'text': 'Nueva versión de la pregunta',
                    'difficulty': 3,
                    'explanation': 'Nueva explicación.',
                    'score': 15,
                    'category': 1,
                    'question_type': 1,
                    'answer_options': [
                        {'text': 'Opción 1', 'correct': False},
                        {'text': 'Opción 2', 'correct': True}
                    ]
                }, request_only=True)]
)
class QuestionEditView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Pregunta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        if question.created_by != request.user:
            return Response({"error": "No tienes permiso para editar esta pregunta."}, status=status.HTTP_403_FORBIDDEN)
        serializer = QuestionCreateSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                question.answeroption_set.all().delete()
                updated_question = serializer.save()
            return Response(QuestionCreateSerializer(updated_question).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Listar preguntas",
    description="Lista todas las preguntas disponibles, permitiendo filtrar por categoría y/o tipo de pregunta.",
    parameters=[
        OpenApiParameter("category", OpenApiTypes.INT, description="ID de la categoría", required=False),
        OpenApiParameter("question_type", OpenApiTypes.INT, description="ID del tipo de pregunta", required=False)
    ],
    responses={200: QuestionStatementSerializer(many=True)},
    tags=["Questions"]
)
class QuestionListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionStatementSerializer
    def get_queryset(self):
        queryset = Question.objects.all()
        category = self.request.query_params.get('category')
        question_type = self.request.query_params.get('question_type')
        if category:
            queryset = queryset.filter(category_id=category)
        if question_type:
            queryset = queryset.filter(question_type_id=question_type)
        return queryset

@extend_schema(
    summary="Resultado de test",
    description="Devuelve el resultado final del test a partir de la participación del usuario.",
    # parameters=[OpenApiParameter("participation_id", OpenApiTypes.INT, description="ID de la participación", required=True)],
    responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
    tags=["Tests"]
)
class TestResultView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, participation_id):
        try:
            participation = TestParticipation.objects.get(id=participation_id, user=request.user)
        except TestParticipation.DoesNotExist:
            return Response({"error": "Participación no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        responses = ParticipationResponse.objects.filter(test_participation=participation)
        correct_count = sum(1 for resp in responses if resp.answer_option.correct)
        total_questions = TestQuestion.objects.filter(test=participation.test).count()
        data = {"total_score": participation.score, "correct_answers": correct_count, "total_questions": total_questions}
        return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Administrar tipos de pregunta",
    description="Devuelve una lista de todos los tipos de pregunta. Sólo accesible por administradores.",
    tags=["Question Types"]
)
class QuestionTypeView(ModelViewSet):
    queryset = QuestionType.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = QuestionTypeSerializer


