<template>
    <div class="review-container">
      <div class="review-card">
        <h2>Revisión de Respuestas{{ category ? ` de ${category}` : '' }}{{ difficulty ? `, Dificultad: ${difficulty}` : '' }}</h2>
        <div v-for="(answer, index) in userAnswers" :key="index" class="answer-item">
          <p><strong>Pregunta {{ index + 1 }}:</strong> {{ answer.question.text }}</p>
          <p><strong>Respuesta Correcta:</strong> {{ getCorrectAnswer(answer.question) }}</p>
          <p><strong>Tu Respuesta:</strong> {{ answer.selectedOption.text }}</p>
          <p><strong>Resultado:</strong> {{ answer.selectedOption.correct ? 'Correcto' : 'Incorrecto' }}</p>
          <p><strong>Puntos Obtenidos:</strong> {{ answer.points }}</p>
          <hr />
        </div>
        <button class="back-btn" @click="goBack">Volver al Inicio</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  
  export default {
    name: 'RevisarRespuestas',
    setup() {
      const router = useRouter();
      const route = useRoute();
      const userAnswers = ref([]);
      const category = ref('');
      const difficulty = ref('');
  
      const getCorrectAnswer = (question) => {
        const correctOption = question.answer_options.find((option) => option.correct);
        return correctOption ? correctOption.text : 'No disponible';
      };
  
      onMounted(() => {
        userAnswers.value = JSON.parse(route.query.answers || '[]');
        category.value = route.query.category || '';
        difficulty.value = route.query.difficulty || '';
      });
  
      const goBack = () => {
        router.push('/mainform');
      };
  
      return {
        userAnswers,
        category,
        difficulty,
        getCorrectAnswer,
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
  
  .review-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-image: url('@/assets/patrones.png');
    padding: 20px;
  }
  
  .review-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 30px;
    width: 100%;
    max-width: 600px;
  }
  
  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .answer-item {
    margin-bottom: 20px;
  }
  
  p {
    font-size: 1.1rem;
    margin: 5px 0;
  }
  
  hr {
    border: 0;
    border-top: 1px solid #ddd;
    margin: 10px 0;
  }
  
  .back-btn {
    padding: 15px 30px;
    background-color: #6d004d;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    display: block;
    margin: 20px auto 0;
  }
  
  .back-btn:hover {
    background-color: #52003b;
  }
  </style>