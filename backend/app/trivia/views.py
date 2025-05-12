import random
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
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
    summary="Recuperar enunciado de pregunta y registrar acceso",
    description=(
        "Valida la participación, obtiene la pregunta por su número, "
        "crea un registro en ParticipationResponse (solo con accessed_at) "
        "y devuelve el enunciado y opciones."
    ),
    parameters=[
        OpenApiParameter("participation_id", OpenApiTypes.INT, description="ID de la participación", required=True),
        OpenApiParameter("question_number", OpenApiTypes.INT, description="Número secuencial de la pregunta", required=True),
    ],
    responses={200: QuestionStatementSerializer, 404: OpenApiTypes.OBJECT},
    tags=["Tests"]
)
class QuestionRetrieveAndAccessView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, participation_id, question_number):
        try:
            participation = TestParticipation.objects.get(
                id=participation_id,
                user=request.user
            )
        except TestParticipation.DoesNotExist:
            return Response(
                {"error": "Participación no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            test_question = TestQuestion.objects.get(
                test=participation.test,
                question_number=question_number
            )
        except TestQuestion.DoesNotExist:
            return Response(
                {"error": "Pregunta no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        ParticipationResponse.objects.create(
            test_participation=participation,
            test_question=test_question
        )

        serializer = QuestionStatementSerializer(test_question.question)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Envío de respuesta y registro de puntuación",
    description=(
        "Actualiza ParticipationResponse con la opción, el tiempo y la puntuación dinámica, "
        "actualiza TestParticipation.score y devuelve el resultado."
    ),
    parameters=[
        OpenApiParameter("participation_id", OpenApiTypes.INT, description="ID de la participación", required=True),
        OpenApiParameter("question_number", OpenApiTypes.INT, description="Número de la pregunta", required=True),
    ],
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

        now = timezone.now()
        deadline = participation.started_at + timezone.timedelta(minutes=participation.test.time_limit_minutes)
        if now > deadline:
            return Response({"error": "Se ha excedido el límite de tiempo del test."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            test_question = TestQuestion.objects.get(test=participation.test, question_number=question_number)
        except TestQuestion.DoesNotExist:
            return Response({"error": "Pregunta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        try:
            answer_option = AnswerOption.objects.get(
                id=serializer.validated_data['answer_option'],
                question=test_question.question
            )
        except AnswerOption.DoesNotExist:
            return Response({"error": "Opción inválida."}, status=status.HTTP_400_BAD_REQUEST)

        is_correct  = answer_option.correct
        question_score = test_question.question.score

        with transaction.atomic():
            try:
                resp = ParticipationResponse.objects.get(
                    test_participation=participation,
                    test_question=test_question,
                    responded_at__isnull=True
                )
            except ParticipationResponse.DoesNotExist:
                return Response({"error": "Acceso no registrado o ya respondido."}, status=status.HTTP_400_BAD_REQUEST)

            resp.answer_option = answer_option
            resp.responded_at  = now

            total_seconds       = participation.test.time_limit_minutes * 60
            num_questions       = TestQuestion.objects.filter(test=participation.test).count()
            per_question_secs   = total_seconds / num_questions
            elapsed_secs        = (resp.responded_at - resp.accessed_at).total_seconds()

            if is_correct and elapsed_secs <= per_question_secs:
                remaining = per_question_secs - elapsed_secs
                if remaining < 1:
                    remaining = 1
                dyn_portion = question_score * remaining / per_question_secs
                earned = 0.5 * question_score + dyn_portion
            else:
                earned = 0.0

            resp.score = earned
            resp.save(update_fields=['answer_option', 'responded_at', 'score'])

            if is_correct:
                participation.score += earned
                participation.save(update_fields=['score'])

        data = {
            "is_correct": is_correct,
            "explanation": test_question.question.explanation, 
            "earned_score": earned,}
        
        total = TestQuestion.objects.filter(test=participation.test).count()
        if question_number == total:
            responses = ParticipationResponse.objects.filter(test_participation=participation)
            correct_count = sum(1 for r in responses if r.answer_option.correct)
            data["final_result"] = {
                "total_score": participation.score,
                "correct_answers": correct_count,
                "total_questions": total
            }

        return Response(AnswerSubmissionResponseSerializer(data).data, status=status.HTTP_200_OK)    

class CategoryViewSet(ModelViewSet):
    """
    ViewSet para gestionar categorías:
    - list:   Listado público de todas las categorías.
    - retrieve: Detalle de una categoría (opcional).
    - create:  Sólo administradores pueden crear.
    - update:  Sólo administradores pueden modificar.
    - destroy: Sólo administradores pueden eliminar.
    """
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly] 
    serializer_class = CategorySerializer
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAdminUser()]
    #     return [AllowAny()]
    
    @extend_schema(
        summary="Listar categorías",
        description="Recupera todas las categorías existentes.",
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear categoría",
        description="Crea una nueva categoría. Sólo el administrador puede acceder a este endpoint.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: OpenApiTypes.OBJECT
        },
        tags=["Categories"],
        examples=[
            OpenApiExample(
                'Ejemplo de creación',
                value={'name': 'Matemáticas', 'description': 'Preguntas de matemáticas'},
                request_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Detalle de categoría",
        description="Recupera la información de una categoría por su ID.",
        responses={200: CategorySerializer, 404: OpenApiTypes.OBJECT},
        tags=["Categories"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar categoría",
        description="Permite al administrador modificar una categoría existente.",
        request=CategorySerializer,
        responses={200: CategorySerializer, 400: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        tags=["Categories"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar categoría",
        description="Permite al administrador eliminar una categoría.",
        responses={204: OpenApiTypes.NONE, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        tags=["Categories"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
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
    summary="Listar preguntas con filtros avanzados",
    description=(
        "Recupera todas las preguntas, permitiendo filtrar opcionalmente por:\n"
        "- `category`: ID de la categoría (exacto).\n"
        "- `question_type`: ID del tipo de pregunta (exacto).\n"
        "- `difficulty_min`: dificultad mínima (inclusive).\n"
        "- `difficulty_max`: dificultad máxima (inclusive).\n\n"
        "Si se envían ambos límites (`difficulty_min` y `difficulty_max`), "
        "se devuelven solo las preguntas cuya dificultad esté entre ambos valores.\n"
        "Si se envía solo uno de los límites, se aplica el filtro correspondiente."
    ),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filtrar por ID de categoría"
        ),
        OpenApiParameter(
            name="question_type",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filtrar por ID de tipo de pregunta"
        ),
        OpenApiParameter(
            name="difficulty_min",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Dificultad mínima (>=)"
        ),
        OpenApiParameter(
            name="difficulty_max",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Dificultad máxima (<=)"
        ),
    ],
    responses={200: QuestionStatementSerializer(many=True)},
    tags=["Questions"],
)
class QuestionListView(ListAPIView):
    """
    Lista todas las preguntas y permite filtrar por:
    - category:       ID de categoría
    - question_type:  ID de tipo de pregunta
    - difficulty_min: Límite inferior de dificultad (>=)
    - difficulty_max: Límite superior de dificultad (<=)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionCreateSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        params = self.request.query_params

        category      = params.get('category')
        question_type = params.get('question_type')
        lower         = params.get('difficulty_min')
        upper         = params.get('difficulty_max')

        if category:
            queryset = queryset.filter(category_id=category)
        if question_type:
            queryset = queryset.filter(question_type_id=question_type)

        if lower is not None and upper is not None:
            queryset = queryset.filter(difficulty__gte=lower, difficulty__lte=upper)
        elif lower is not None:
            queryset = queryset.filter(difficulty__gte=lower)
        elif upper is not None:
            queryset = queryset.filter(difficulty__lte=upper)

        return queryset

@extend_schema(
    summary="Eliminar pregunta",
    description="Permite eliminar una pregunta creada por el usuario. Solo el creador (campo created_by) puede eliminar la pregunta.",
    request=QuestionCreateSerializer,
    tags=["Questions"],
)
class QuestionDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = QuestionCreateSerializer
    def delete(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Pregunta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        if question.created_by != request.user:
            return Response({"error": "No tienes permiso para eliminar esta pregunta."}, status=status.HTTP_403_FORBIDDEN)
        
        if question.test_question.exists():
            return Response({"error": "Esta pregunta está vinculada a un test y no se puede borrar"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            question.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


