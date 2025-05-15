```vue
<template>
  <div class="quiz-container">
    <div class="quiz-card">
      <h2>Cuestionario de {{ category || 'Categoría' }}</h2>
      <div v-if="currentQuestion">
        <div class="timer-bar">
          <div :style="{ width: questionTimerProgress + '%' }"></div>
        </div>
        <p class="question">{{ currentQuestion.text }}</p>
        <div class="options">
          <button
            v-for="(option, index) in shuffledOptions"
            :key="index"
            @click="selectAnswer(option)"
            :class="{
              'option-btn': true,
              selected: selectedOption === option,
              correct: selectedOption === option && isAnswered && option.correct,
              incorrect: selectedOption === option && isAnswered && !option.correct
            }"
            :disabled="isAnswered"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
      <div v-else-if="!loading && !currentQuestion && !quizFinished && !errorMessage">
        <p>No hay preguntas disponibles para la categoría de {{ category }}.</p>
        <button class="result-btn" @click="router.push('/mainform')">Volver</button>
      </div>
      <div v-else-if="quizFinished">
        <p>¡Cuestionario completado!</p>
        <button class="result-btn" @click="goToResults">Ver Resultados</button>
      </div>
      <div v-if="loading && !errorMessage">
        <p>Cargando pregunta...</p>
      </div>
      <div v-if="errorMessage">
        <p class="error">{{ errorMessage }}</p>
        <button class="result-btn" @click="router.push('/mainform')">Volver</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'QuizGeneric',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const currentQuestion = ref(null);
    const currentQuestionNumber = ref(1);
    const loading = ref(true);
    const quizFinished = ref(false);
    const selectedOption = ref(null);
    const isAnswered = ref(false);
    const userAnswers = ref([]);
    const questionTimer = ref(10); // 10-second timer per question
    const questionTimerInterval = ref(null);
    const score = ref(0);
    const category = ref('');
    const participationId = ref(null);
    const errorMessage = ref('');

    const shuffledOptions = computed(() => {
      if (!currentQuestion.value) return [];
      const options = [...currentQuestion.value.answer_options];
      return options.sort(() => Math.random() - 0.5);
    });

    const questionTimerProgress = computed(() =>
      questionTimer.value > 0 ? (questionTimer.value / 10) * 100 : 0
    );

    const createTest = async (categoryId, difficulty) => {
      console.log('Creating test with:', { categoryId, difficulty });
      const token = localStorage.getItem('token');
      console.log('Token for test creation:', token ? token : 'Missing');
      if (!token) {
        console.error('No token available for test creation');
        errorMessage.value = 'Debes iniciar sesión primero. Redirigiendo...';
        setTimeout(() => router.push('/login'), 2000);
        return false;
      }

      try {
        const response = await fetch('http://localhost:8080/trivia/tests/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Token ${token}`
          },
          body: JSON.stringify({
            category: parseInt(categoryId),
            time_limit_minutes: 10,
            difficulty: difficulty || 'Fácil',
            n: 10 // 10 preguntas
          })
        });
        console.log('Create test response status:', response.status);
        if (response.ok) {
          const data = await response.json();
          console.log('Test creation response:', data);
          participationId.value = data.participation_id;
          console.log('Test created, participationId:', participationId.value);
          return true;
        } else {
          const errorText = await response.text();
          console.error('Error creating test:', response.status, errorText);
          errorMessage.value = `No se pudo crear el cuestionario: ${response.status} ${errorText}`;
          if (response.status === 401) {
            errorMessage.value += ' Token inválido, por favor inicia sesión nuevamente.';
            setTimeout(() => router.push('/login'), 2000);
          }
          return false;
        }
      } catch (error) {
        console.error('Connection error creating test:', error);
        errorMessage.value = 'Error de conexión al crear el cuestionario.';
        return false;
      }
    };

    const fetchQuestion = async (questionNumber) => {
      console.log('Fetching question number:', questionNumber, 'for participationId:', participationId.value);
      const token = localStorage.getItem('token');
      console.log('Token for fetch question:', token ? token : 'Missing');
      if (!token) {
        console.error('No token available for fetching question');
        errorMessage.value = 'Debes iniciar sesión primero. Redirigiendo...';
        setTimeout(() => router.push('/login'), 2000);
        return false;
      }

      try {
        const response = await fetch(
          `http://localhost:8080/trivia/tests/${participationId.value}/question/${questionNumber}/`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Token ${token}`
            },
            method: 'GET'
          }
        );
        console.log('Fetch question response status:', response.status);
        if (response.ok) {
          currentQuestion.value = await response.json();
          console.log('Question fetched:', JSON.stringify(currentQuestion.value, null, 2));
          return true;
        } else if (response.status === 404) {
          console.log('No more questions, ending quiz');
          quizFinished.value = true;
          clearInterval(questionTimerInterval.value);
          return false;
        } else {
          const errorText = await response.text();
          console.error('Error fetching question:', response.status, errorText);
          errorMessage.value = `Error al cargar la pregunta: ${response.status} ${errorText}`;
          if (response.status === 401) {
            errorMessage.value += ' Token inválido, por favor inicia sesión nuevamente.';
            setTimeout(() => router.push('/login'), 2000);
          }
          return false;
        }
      } catch (error) {
        console.error('Connection error fetching question:', error);
        errorMessage.value = 'Error de conexión al cargar la pregunta.';
        return false;
      }
    };

    const submitAnswer = async (option) => {
      console.log('Submitting answer for question:', currentQuestionNumber.value, 'option:', JSON.stringify(option, null, 2));
      try {
        const token = localStorage.getItem('token');
        console.log('Submit answer token:', token ? token : 'Missing');
        if (!token) {
          console.error('No token available for submitting answer');
          errorMessage.value = 'Debes iniciar sesión primero. Redirigiendo...';
          setTimeout(() => router.push('/login'), 2000);
          return 0;
        }

        const response = await fetch(
          `http://localhost:8080/trivia/tests/${participationId.value}/question/${currentQuestionNumber.value}/answer/`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'Authorization': `Token ${token}`
            },
            body: JSON.stringify({
              answer_option: option.id
            })
          }
        );
        console.log('Submit answer response status:', response.status);
        if (response.ok) {
          const data = await response.json();
          const points = data.points || 0; // Usar 0 si points no está definido
          option.correct = points > 0; // Establecer correct basado en puntos
          console.log('Answer submitted, points:', points, 'correct:', option.correct);
          return points;
        } else {
          const errorText = await response.text();
          console.error('Error submitting answer:', response.status, errorText);
          errorMessage.value = `-error al enviar la respuesta: ${response.status} ${errorText}`;
          if (response.status === 401) {
            errorMessage.value += ' Token inválido, por favor inicia sesión nuevamente.';
            setTimeout(() => router.push('/login'), 2000);
          } else if (response.status === 400) {
            errorMessage.value += ' Verifica que la opción seleccionada sea válida.';
            setTimeout(() => router.push('/mainform'), 2000);
          }
          return 0;
        }
      } catch (error) {
        console.error('Connection error submitting answer:', error);
        errorMessage.value = 'Error de conexión al enviar la respuesta.';
        return 0;
      }
    };

    const startQuestionTimer = () => {
      questionTimer.value = 10;
      console.log('Starting question timer with:', questionTimer.value, 'seconds');
      clearInterval(questionTimerInterval.value); // Clear any existing interval
      questionTimerInterval.value = setInterval(() => {
        questionTimer.value -= 1;
        if (questionTimer.value <= 0) {
          console.log('Question timer expired, moving to next question');
          clearInterval(questionTimerInterval.value);
          nextQuestion();
        }
      }, 1000);
    };

    const selectAnswer = async (option) => {
      if (isAnswered.value) return;
      isAnswered.value = true;
      selectedOption.value = option;
      clearInterval(questionTimerInterval.value); // Stop timer on answer selection

      const points = await submitAnswer(option);
      score.value += points;

      userAnswers.value.push({
        question: {
          text: currentQuestion.value.text,
          answer_options: [...currentQuestion.value.answer_options] // Copia completa
        },
        selectedOption: { ...option }, // Copia de la opción seleccionada
        points
      });
      console.log('User answer added:', JSON.stringify(userAnswers.value[userAnswers.value.length - 1], null, 2));

      setTimeout(nextQuestion, 2000); // 2 segundos para mostrar retroalimentación
    };

    const nextQuestion = async () => {
      console.log('Moving to next question');
      selectedOption.value = null;
      isAnswered.value = false;
      
      // Verificar si se ha alcanzado el límite de 10 preguntas
      if (currentQuestionNumber.value >= 10) {
        console.log('Reached 10 questions, ending quiz');
        quizFinished.value = true;
        clearInterval(questionTimerInterval.value);
        // Redirigir automáticamente a Resultados.vue
        await goToResults();
        return;
      }

      currentQuestionNumber.value += 1;
      loading.value = true;

      const questionFetched = await fetchQuestion(currentQuestionNumber.value);
      loading.value = false;
      if (questionFetched) {
        startQuestionTimer(); // Start timer for new question
      } else {
        quizFinished.value = true;
        clearInterval(questionTimerInterval.value);
        await goToResults(); // Redirigir si no hay más preguntas
      }
    };

    const goToResults = async () => {
      console.log('Fetching results for participationId:', participationId.value);
      console.log('Sending to results:', { score: score.value, answers: userAnswers.value });
      try {
        const token = localStorage.getItem('token');
        console.log('Token for fetch results:', token ? token : 'Missing');
        if (!token) {
          console.error('No token available for fetching results');
          errorMessage.value = 'Debes iniciar sesión primero. Redirigiendo...';
          setTimeout(() => router.push('/login'), 2000);
          return;
        }

        const response = await fetch(
          `http://localhost:8080/trivia/tests/${participationId.value}/result/`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Token ${token}`
            },
            method: 'GET'
          }
        );
        console.log('Fetch results response status:', response.status);
        if (response.ok) {
          const data = await response.json();
          console.log('Results fetched:', data);
          router.push({
            path: '/resultados',
            query: {
              score: score.value, // Usar score local para consistencia
              answers: JSON.stringify(userAnswers.value), // Usar userAnswers local
              category: category.value,
              testId: participationId.value,
              difficulty: route.query.difficulty || 'Fácil'
            }
          });
        } else {
          const errorText = await response.text();
          console.error('Error fetching results:', response.status, errorText);
          errorMessage.value = `Error al cargar los resultados: ${response.status} ${errorText}`;
          if (response.status === 401) {
            errorMessage.value += ' Token inválido, por favor inicia sesión nuevamente.';
            setTimeout(() => router.push('/login'), 2000);
          }
        }
      } catch (error) {
        console.error('Connection error fetching results:', error);
        errorMessage.value = 'Error de conexión al cargar los resultados.';
      }
    };

    onMounted(async () => {
      console.log('QuizGeneric mounted, route query:', route.query);
      const token = localStorage.getItem('token');
      console.log('Token on mount:', token ? token : 'Missing');
      if (!token) {
        console.error('No token available on mount');
        errorMessage.value = 'Debes iniciar sesión primero. Redirigiendo...';
        setTimeout(() => router.push('/login'), 2000);
        return;
      }

      const categoryId = route.query.categoryId;
      const difficulty = route.query.difficulty;
      category.value = route.query.categoryName || 'Categoría';
      console.log('CategoryId:', categoryId, 'Category:', category.value, 'Difficulty:', difficulty);

      if (!categoryId) {
        console.error('No categoryId provided');
        errorMessage.value = 'Categoría no especificada.';
        loading.value = false;
        setTimeout(() => router.push('/mainform'), 2000);
        return;
      }

      loading.value = true;
      const testCreated = await createTest(categoryId, difficulty);
      if (!testCreated) {
        loading.value = false;
        return;
      }

      const questionFetched = await fetchQuestion(currentQuestionNumber.value);
      loading.value = false;
      if (questionFetched) {
        startQuestionTimer();
      }
    });

    onUnmounted(() => {
      console.log('QuizGeneric unmounted, clearing timer');
      clearInterval(questionTimerInterval.value);
    });

    return {
      currentQuestion,
      shuffledOptions,
      loading,
      quizFinished,
      selectedOption,
      isAnswered,
      questionTimerProgress,
      selectAnswer,
      goToResults,
      category,
      errorMessage,
      router
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
}

.quiz-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/patrones.png');
  padding: 20px;
}

.quiz-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 600px;
  text-align: center;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.question {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  padding: 10px;
  background-color: #338bff;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.option-btn:hover:not(.selected):not(.correct):not(.incorrect) {
  background-color: #7c716d;
}

.option-btn.selected.correct {
  background-color: #05ab68;
}

.option-btn.selected.incorrect {
  background-color: #ff3333;
}

.option-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.result-btn {
  padding: 15px 30px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 20px;
}

.result-btn:hover {
  background-color: #52003b;
}

.timer-bar {
  width: 100%;
  height: 10px;
  background-color: #ddd;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 20px;
}

.timer-bar div {
  height: 100%;
  background-color: #2ecc71;
  transition: width 1s linear;
}

.error {
  color: #ff3333;
  font-size: 1.2rem;
  margin-bottom: 20px;
}
</style>
```