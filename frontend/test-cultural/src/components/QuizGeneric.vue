<template>
    <div class="quiz-container">
      <div class="quiz-card">
        <h2>Cuestionario de {{ category || 'Categoría' }}</h2>
        <p>Dificultad: {{ difficulty || 'Fácil' }}</p>
        <p>Puntuación: {{ score }} puntos</p>
        <div v-if="questions.length && currentQuestionIndex < questions.length">
          <h3>Pregunta {{ currentQuestionIndex + 1 }} de {{ questions.length }}</h3>
          <p>{{ currentQuestion.text }}</p>
          <div class="options">
            <button
              v-for="(option, index) in currentQuestion.answer_options"
              :key="index"
              class="option-btn"
              :disabled="selectedOption !== null"
              @click="selectOption(option)"
            >
              {{ option.text }}
            </button>
          </div>
          <button
            v-if="selectedOption !== null"
            class="next-btn"
            @click="nextQuestion"
          >
            Siguiente
          </button>
        </div>
        <p v-else-if="questions.length === 0">No hay preguntas disponibles.</p>
        <p v-else>Cuestionario completado. Redirigiendo a resultados...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  
  export default {
    name: 'QuizGeneric',
    setup() {
      const router = useRouter();
      const route = useRoute();
      const questions = ref([]);
      const category = ref('');
      const difficulty = ref('');
      const currentQuestionIndex = ref(0);
      const score = ref(0);
      const userAnswers = ref([]);
      const selectedOption = ref(null);
  
      const currentQuestion = computed(() =>
        questions.value[currentQuestionIndex.value]
      );
  
      onMounted(() => {
        // Parse query parameters
        category.value = route.query.category || '';
        difficulty.value = route.query.difficulty || 'Fácil';
        try {
          questions.value = JSON.parse(route.query.questions || '[]');
        } catch (error) {
          console.error('Error al parsear preguntas:', error);
          alert('Error al cargar las preguntas.');
        }
  
        // Redirect to mainform if no questions
        if (questions.value.length === 0) {
          alert('No hay preguntas disponibles para esta categoría y dificultad.');
          router.push('/mainform');
        }
      });
  
      const selectOption = (option) => {
        if (selectedOption.value !== null) return;
        selectedOption.value = option;
        const points = option.correct ? 10 : 0;
        score.value += points;
        userAnswers.value.push({
          question: currentQuestion.value,
          selectedOption: option,
          points
        });
      };
  
      const nextQuestion = () => {
        selectedOption.value = null;
        currentQuestionIndex.value++;
        if (currentQuestionIndex.value >= questions.value.length) {
          // Navigate to results
          router.push({
            path: '/resultados',
            query: {
              score: score.value,
              answers: JSON.stringify(userAnswers.value),
              category: category.value,
              difficulty: difficulty.value
            }
          });
        }
      };
  
      return {
        questions,
        category,
        difficulty,
        currentQuestionIndex,
        currentQuestion,
        score,
        userAnswers,
        selectedOption,
        selectOption,
        nextQuestion
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
    background-size: cover;
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
    margin-bottom: 15px;
  }
  
  h3 {
    color: #2c3e50;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 1.2rem;
    margin-bottom: 15px;
  }
  
  .options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .option-btn {
    padding: 12px 20px;
    background-color: #6d004d;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .option-btn:hover:not(:disabled) {
    background-color: #52003b;
  }
  
  .option-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .next-btn {
    padding: 15px 30px;
    background-color: #05ab68;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .next-btn:hover {
    background-color: #7c716d;
  }
  </style>