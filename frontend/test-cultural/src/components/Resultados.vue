<template>
    <div class="results-container">
      <div class="results-card">
        <h2>Resultados del Cuestionario{{ category ? ` de ${category}` : '' }}{{ difficulty ? `, Dificultad: ${difficulty}` : '' }}</h2>
        <p>Puntuación Total: {{ score }} puntos</p>
        <p>Preguntas Correctas: {{ correctAnswers }} / {{ totalQuestions }}</p>
        <button class="review-btn" @click="goToReview">Revisar Respuestas</button>
        <button class="back-btn" @click="goBack">Volver al Inicio</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  
  export default {
    name: 'QuizResultados',
    setup() {
      const router = useRouter();
      const route = useRoute();
      const score = ref(0);
      const userAnswers = ref([]);
      const category = ref('');
      const difficulty = ref('');
      const correctAnswers = computed(() =>
        userAnswers.value.filter((answer) => answer.selectedOption.correct).length
      );
      const totalQuestions = computed(() => userAnswers.value.length);
  
      onMounted(() => {
        score.value = parseInt(route.query.score) || 0;
        userAnswers.value = JSON.parse(route.query.answers || '[]');
        category.value = route.query.category || '';
        difficulty.value = route.query.difficulty || '';
      });
  
      const goToReview = () => {
        router.push({
          path: '/revisar-respuestas',
          query: { answers: JSON.stringify(userAnswers.value) },
        });
      };
  
      const goBack = () => {
        router.push('/mainform');
      };
  
      return {
        score,
        userAnswers,
        category,
        difficulty,
        correctAnswers,
        totalQuestions,
        goToReview,
        goBack,
      };
    },
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
  
  * {
    font-family: 'Jeju Hallasan', cursive;
  }
  
  .results-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-image: url('@/assets/patrones.png');
    padding: 20px;
  }
  
  .results-card {
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
  
  p {
    font-size: 1.2rem;
    margin-bottom: 15px;
  }
  
  .review-btn,
  .back-btn {
    padding: 15px 30px;
    background-color: #6d004d;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    margin: 10px;
  }
  
  .review-btn:hover,
  .back-btn:hover {
    background-color: #52003b;
  }
  </style>