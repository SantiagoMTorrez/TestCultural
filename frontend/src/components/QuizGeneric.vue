<template>
  <div class="quiz-container">
    <div class="quiz-card">
      <h2>Cuestionario de {{ category }}</h2>

      <!-- Feedback Notifications -->
      <GreatingNotification v-if="showGreet" :message="greetMessage" />
      <FailedNotification   v-if="showFail"  :message="failMessage" />

      <template v-if="loading">
        <p>Cargando pregunta...</p>
      </template>

      <template v-else-if="errorMessage">
        <p class="error">{{ errorMessage }}</p>
        <button class="result-btn" @click="goHome">Volver</button>
      </template>

      <!-- Muestra pregunta mientras no haya acabado -->
      <template v-else-if="!quizFinished">
        <template v-if="currentQuestion">
          <TimerBar :duration="questionTimerDuration" :reverse="true" />
          <p class="question">{{ currentQuestion.text }}</p>

          <div class="options">
            <OptionButton
              v-for="option in shuffledOptions"
              :key="option.id"
              :option="option"
              :selected="selectedOption === option"
              :isAnswered="isAnswered"
              @select="handleSelect"
            />
          </div>
        </template>
        <template v-else>
          <p>No hay preguntas disponibles para {{ category }}.</p>
          <button class="result-btn" @click="goHome">Volver</button>
        </template>
      </template>

      <!-- Scoreboard al terminar las n preguntas -->
      <template v-else>
        <div class="scoreboard">
          <h3>Resultados Finales</h3>
          <p><strong>Puntuación final:</strong> {{  parseFloat(finalResult?.total_score).toFixed(0) ?? score.toFixed(0) }}</p>
          <p><strong>Preguntas totales:</strong> {{ totalQuestions }}</p>
          <p><strong>Correctas:</strong> {{ finalResult?.correct_answers ?? '-' }}</p>
          <p><strong>Incorrectas:</strong> {{ totalQuestions - finalResult?.correct_answers ?? '-' }}</p>
          <button class="result-btn" @click="goToResults">Ver detalle de respuestas</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import TimerBar from './TimerBar.vue';
import OptionButton from './OptionButton.vue';
import GreatingNotification from './GreatingNotification.vue';
import FailedNotification from './FailedNotification.vue';

export default {
  name: 'QuizGeneric',
  components: { TimerBar, OptionButton, GreatingNotification, FailedNotification },
  setup() {
    const router = useRouter();
    const route  = useRoute();

    // Parámetros y estado
    const loading               = ref(true);
    const errorMessage          = ref('');
    const category              = ref(route.query.categoryName || 'Categoría');
    const participationId       = ref(null);
    const currentQuestion       = ref(null);
    const selectedOption        = ref(null);
    const isAnswered            = ref(false);
    const quizFinished          = ref(false);
    const score                 = ref(0);
    const userAnswers           = ref([]);
    const questionTimer         = ref(10);
    const questionDuration      = ref(10);
    const currentQuestionNumber = ref(1);
    const showGreet             = ref(false);
    const greetMessage          = ref('');
    const showFail              = ref(false);
    const failMessage           = ref('');
    const finalResult           = ref(null);

    // Número total de preguntas
    const totalQuestions = parseInt(route.query.n, 10);

    let questionInterval = null;

    // Opciones mezcladas y progreso de la barra
    const shuffledOptions = computed(() =>
      currentQuestion.value
        ? [...currentQuestion.value.answer_options].sort(() => Math.random() - 0.5)
        : []
    );
    const questionTimerDuration = computed(() => (questionDuration.value));

    // Crear test inicial
    async function createTest(cid, diff, n) {
      const token = localStorage.getItem('token');
      if (!token) {
        errorMessage.value = 'Debes iniciar sesión primero.';
        setTimeout(() => router.push('/login'), 2000);
        return false;
      }
      const resp = await fetch(`http://${window.location.hostname}:8080/trivia/tests/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          category: parseInt(cid, 10),
          time_limit_minutes: 10,
          difficulty: diff,
          n
        })
      });
      if (!resp.ok) {
        const txt = await resp.text();
        errorMessage.value = `Error creando test: ${resp.status} ${txt}`;
        if (resp.status === 401) setTimeout(() => router.push('/login'), 2000);
        return false;
      }
      participationId.value = (await resp.json()).participation_id;
      return true;
    }

    // Traer pregunta por número
    async function fetchQuestion(num) {
      const token = localStorage.getItem('token');
      if (!token) { router.push('/login'); return false; }
      const resp = await fetch(
        `http://${window.location.hostname}:8080/trivia/tests/${participationId.value}/question/${num}/start`,
        { headers: { 'Accept': 'application/json', 'Authorization': `Token ${token}` } }
      );
      if (resp.status === 404) {
        // Si no hay más preguntas
        return false;
      }
      if (!resp.ok) {
        errorMessage.value = `Error cargando: ${resp.status}`;
        return false;
      }
      currentQuestion.value = await resp.json();
      questionDuration.value = 20;
      return true;
    }

    // Enviar respuesta y obtener puntos
    async function submitAnswer(option) {
      const token = localStorage.getItem('token');
      const resp = await fetch(
        `http://${window.location.hostname}:8080/trivia/tests/${participationId.value}/question/${currentQuestionNumber.value}/answer/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          },
          body: JSON.stringify({ answer_option: option.id })
        }
      );
      if (!resp.ok) return 0;
      const data = await resp.json();
      return data.earned_score || 0;
    }

    // Inicio de temporizador
    function startTimer() {
      questionTimer.value = 10;
      clearInterval(questionInterval);
      questionInterval = setInterval(() => {
        questionTimer.value--;
        if (questionTimer.value <= 0) nextQuestion();
      }, 1000);
    }

    // Selector de opción
    async function handleSelect(option) {
      if (isAnswered.value) return;
      isAnswered.value = true;
      selectedOption.value = option;
      clearInterval(questionInterval);

      const pts = await submitAnswer(option);
      score.value += pts;
      userAnswers.value.push({ question: currentQuestion.value, option, points: pts });

      if (pts > 0) {
        greetMessage.value = `¡Correcto! +${pts.toFixed(0)} pts`;
        showGreet.value = true;
        await new Promise(r => setTimeout(r, 2000));
        showGreet.value = false;
      } else {
        failMessage.value = currentQuestion.value.explanation || 'Incorrecto';
        showFail.value = true;
        await new Promise(r => setTimeout(r, 2000));
        showFail.value = false;
      }

      await nextQuestion();
    }

    // Avanzar a siguiente o terminar
    async function nextQuestion() {
      clearInterval(questionInterval);
      selectedOption.value = null;
      isAnswered.value = false;

      // Si ya llegamos al límite, finalizamos
      if (currentQuestionNumber.value >= totalQuestions) {
        await finishQuiz();
        return;
      }

      // En otro caso, seguimos
      currentQuestionNumber.value++;
      loading.value = true;
      const ok = await fetchQuestion(currentQuestionNumber.value);
      loading.value = false;
      if (ok) startTimer();
      else await finishQuiz();
    }

    // Obtener resultado final y marcar como terminado
    async function finishQuiz() {
      quizFinished.value = true;
      loading.value = true;
      try {
        const token = localStorage.getItem('token');
        const resp = await fetch(
          `http://${window.location.hostname}:8080/trivia/tests/${participationId.value}/result/`,
          { headers: { 'Authorization': `Token ${token}` } }
        );
        if (!resp.ok) {
          errorMessage.value = `Error obteniendo resultados: ${resp.status}`;
        } else {
          finalResult.value = await resp.json();
        }
      } catch {
        errorMessage.value = 'Error de red al obtener resultados.';
      } finally {
        loading.value = false;
      }
    }

    // Navegación
    const goToResults = () => {
      console.log(userAnswers.value)

      router.push({
        name: 'Results',
        query: {
          participationId: participationId.value,
          n: totalQuestions
        }
      });
    }


    const goHome = () => router.push({ name: 'MainForm' });

    // Ciclo de vida
    onMounted(async () => {
      const { categoryId, difficulty, n } = route.query;
      if (!(await createTest(categoryId, difficulty, parseInt(n, 10)))) return;
      if (await fetchQuestion(currentQuestionNumber.value)) startTimer();
      loading.value = false;
    });

    onUnmounted(() => clearInterval(questionInterval));

    return {
      loading, errorMessage, category, currentQuestion,
      shuffledOptions, selectedOption, isAnswered, quizFinished, handleSelect, goToResults, goHome,
      showGreet, greetMessage, showFail, failMessage,
      totalQuestions, finalResult, score, questionTimerDuration
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
  /* background-image: url('@/assets/patrones.png'); */
  background-image: url('@/assets/patron-move.gif');
  background-size: cover;
  background-repeat: no-repeat;
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