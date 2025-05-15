```vue
<template>
  <div class="results-container">
    <div class="results-card">
      <h2>Resultados del Cuestionario{{ category ? ` de ${category}` : '' }}{{ difficulty ? `, Dificultad: ${difficulty}` : '' }}</h2>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <template v-else>
        <p>Puntuación Total: {{ score }} puntos</p>
        <p>Preguntas Correctas: {{ correctAnswers }} / {{ totalQuestions }}</p>
      </template>
      <button class="review-btn" @click="goToReview" :disabled="errorMessage || totalQuestions === 0">Revisar Respuestas</button>
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
    const errorMessage = ref('');

    const correctAnswers = computed(() => {
      const count = userAnswers.value.filter((answer) => answer.selectedOption?.correct === true).length;
      console.log('Correct answers count:', count, 'from answers:', userAnswers.value);
      return count;
    });
    const totalQuestions = computed(() => userAnswers.value.length);

    onMounted(() => {
      try {
        score.value = parseInt(route.query.score) || 0;
        userAnswers.value = route.query.answers ? JSON.parse(route.query.answers) : [];
        category.value = route.query.category || '';
        difficulty.value = route.query.difficulty || '';
        if (!route.query.score || !route.query.answers || userAnswers.value.length === 0) {
          errorMessage.value = 'No se pudieron cargar los resultados del cuestionario.';
        } else {
          // Validar estructura de userAnswers
          userAnswers.value.forEach((answer, index) => {
            if (!answer.question || !answer.selectedOption || !answer.question.answer_options) {
              console.warn(`Answer ${index + 1} incomplete:`, answer);
              errorMessage.value = 'Algunas respuestas no tienen la información completa.';
            }
          });
        }
      } catch (error) {
        console.error('Error parsing quiz results:', error);
        errorMessage.value = 'Error al cargar los resultados del cuestionario.';
      }
    });

    const goToReview = () => {
      if (errorMessage.value || totalQuestions.value === 0) return;
      console.log('Navigating to review with answers:', userAnswers.value);
      router.push({
        path: '/revisarRespuestas',
        query: {
          answers: JSON.stringify(userAnswers.value),
          category: category.value,
          difficulty: difficulty.value
        }
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
      errorMessage,
      goToReview,
      goBack
    };
  }
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

.error {
  color: #ff3333;
  font-size: 1.2rem;
  margin-bottom: 20px;
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

.review-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.review-btn:hover:not(:disabled),
.back-btn:hover {
  background-color: #52003b;
}
</style>
```