<template>
    <div class="quiz-container">
      <div class="quiz-card">
        <h2>Cuestionario de Historia</h2>
        <div v-if="currentQuestion">
          <div class="timer-bar">
            <div :style="{ width: timerProgress + '%' }"></div>
          </div>
          <p class="question">{{ currentQuestion.text }}</p>
          <div class="options">
            <button
              v-for="(option, index) in shuffledOptions"
              :key="index"
              @click="selectAnswer(option)"
              :class="{ 'option-btn': true, selected: selectedOption === option }"
              :disabled="isAnswered"
            >
              {{ option.text }}
            </button>
          </div>
        </div>
        <div v-else-if="!loading && questions.length === 0">
          <p>No hay preguntas disponibles para la categoría de Historia.</p>
        </div>
        <div v-else-if="quizFinished">
          <p>¡Cuestionario completado!</p>
          <button class="result-btn" @click="goToResults">Ver Resultados</button>
        </div>
        <div v-if="loading">
          <p>Cargando preguntas...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, onUnmounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'QuizHistoria',
    setup() {
      const router = useRouter();
      const questions = ref([]);
      const currentQuestionIndex = ref(0);
      const loading = ref(true);
      const quizFinished = ref(false);
      const selectedOption = ref(null);
      const isAnswered = ref(false);
      const userAnswers = ref([]);
      const timer = ref(10);
      const timerInterval = ref(null);
      const score = ref(0);
  
      const currentQuestion = computed(() =>
        questions.value[currentQuestionIndex.value]
      );
  
      const shuffledOptions = computed(() => {
        if (!currentQuestion.value) return [];
        const options = [...currentQuestion.value.answer_options];
        return options.sort(() => Math.random() - 0.5); // Shuffle options
      });
  
      const timerProgress = computed(() => (timer.value / 10) * 100);
  
      const fetchQuestions = async () => {
        try {
          const response = await fetch('http://localhost:8080/trivia/questions/?category=1', {
            headers: {
              accept: 'application/json',
              Authorization: `Token ${localStorage.getItem('token')}`,
            },
            method: 'GET',
          });
          if (response.ok) {
            questions.value = await response.json();
          } else {
            console.error('Error al obtener preguntas');
          }
        } catch (error) {
          console.error('Error de conexión:', error);
        } finally {
          loading.value = false;
        }
      };
  
      const startTimer = () => {
        timer.value = 10;
        timerInterval.value = setInterval(() => {
          timer.value -= 1;
          if (timer.value <= 0) {
            nextQuestion();
          }
        }, 1000);
      };
  
      const selectAnswer = (option) => {
        if (isAnswered.value) return;
        isAnswered.value = true;
        selectedOption.value = option;
        clearInterval(timerInterval.value);
  
        const points = timer.value * 10; // 10 points per second remaining
        score.value += points;
  
        userAnswers.value.push({
          question: currentQuestion.value,
          selectedOption: option,
          points,
        });
  
        setTimeout(nextQuestion, 1000); // Wait 1 second before moving to next question
      };
  
      const nextQuestion = () => {
        clearInterval(timerInterval.value);
        selectedOption.value = null;
        isAnswered.value = false;
        currentQuestionIndex.value += 1;
  
        if (currentQuestionIndex.value >= questions.value.length) {
          quizFinished.value = true;
        } else {
          startTimer();
        }
      };
  
      const goToResults = () => {
        router.push({
          path: '/resultados',
          query: { score: score.value, answers: JSON.stringify(userAnswers.value) },
        });
      };
  
      onMounted(() => {
        fetchQuestions();
        startTimer();
      });
  
      onUnmounted(() => {
        clearInterval(timerInterval.value);
      });
  
      return {
        questions,
        currentQuestion,
        shuffledOptions,
        loading,
        quizFinished,
        selectedOption,
        isAnswered,
        timerProgress,
        selectAnswer,
        goToResults,
      };
    },
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
  
  .option-btn:hover {
    background-color: #7c716d;
  }
  
  .option-btn.selected {
    background-color: #05ab68;
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
  </style>