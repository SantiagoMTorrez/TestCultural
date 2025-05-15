<template>
  <div class="quiz-container">
    <div v-if="currentQuestion" class="question-card">
      <div class="question-header">
        <h3>Pregunta {{ puntero + 1 }} de 10</h3>
      </div>
      <div class="question-content">
        <h2>{{ currentQuestion.text }}</h2>
        <div class="options-container">
          <button 
            v-for="(option, index) in shuffledOptions" 
            :key="index"
            @click="selectOption(option)"
            :class="{ 'selected': selectedOption === option, 'correct': showFeedback && option.correct, 'incorrect': showFeedback && !option.correct && selectedOption === option }"
            class="option-btn"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
      <button 
        @click="nextQuestion" 
        :disabled="!selectedOption" 
        class="next-btn"
      >
        Siguiente
      </button>
    </div>
    <div v-else class="loading">
      Cargando preguntas...
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'QuizGenericProv',
  setup() {
    const router = useRouter();
    const questions = ref([]);
    const puntero = ref(parseInt(localStorage.getItem('puntero')) || 0);
    const respuestas = ref(parseInt(localStorage.getItem('respuestas')) || 0);
    const selectedOption = ref(null);
    const showFeedback = ref(false);
    const categoryId = localStorage.getItem('idCategoria');

    // Obtener preguntas de la categoría
    onMounted(async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8080/trivia/questions/?category=${categoryId}`, {
          headers: {
            'Authorization': `Token ${token}`,
            'Accept': 'application/json'
          }
        });

        if (response.ok) {
          const allQuestions = await response.json();
          const questionIds = JSON.parse(localStorage.getItem('preguntas') || '[]');
          
          // Filtrar solo las preguntas seleccionadas
          questions.value = allQuestions.filter(q => questionIds.includes(q.id));
        }
      } catch (error) {
        console.error('Error al cargar preguntas:', error);
      }
    });

    // Pregunta actual
    const currentQuestion = computed(() => {
      return questions.value[puntero.value];
    });

    // Opciones mezcladas
    const shuffledOptions = computed(() => {
      if (!currentQuestion.value) return [];
      
      const options = currentQuestion.value.answer_options.map(opt => ({
        text: opt.text,
        correct: opt.correct
      }));
      
      return options.sort(() => Math.random() - 0.5);
    });

    // Seleccionar opción
    const selectOption = (option) => {
      if (showFeedback.value) return;
      selectedOption.value = option;
    };

    // Siguiente pregunta
    const nextQuestion = () => {
      if (selectedOption.value?.correct) {
        respuestas.value++;
        localStorage.setItem('respuestas', respuestas.value);
      }

      showFeedback.value = false;
      selectedOption.value = null;

      if (puntero.value < 9) {
        puntero.value++;
        localStorage.setItem('puntero', puntero.value);
      } else {
        router.push('/finTest');
      }
    };

    return {
      questions,
      puntero,
      currentQuestion,
      shuffledOptions,
      selectedOption,
      showFeedback,
      selectOption,
      nextQuestion,
      respuestas
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

.question-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.question-header {
  margin-bottom: 20px;
  text-align: center;
}

.question-content {
  margin: 30px 0;
}

h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.options-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin-bottom: 30px;
}

.option-btn {
  padding: 15px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-btn:hover:not(:disabled) {
  background-color: #52003b;
}

.option-btn.selected {
  background-color: #338bff;
}

.option-btn.correct {
  background-color: #05ab68;
}

.option-btn.incorrect {
  background-color: #ff3333;
}

.next-btn {
  display: block;
  margin: 0 auto;
  padding: 12px 30px;
  background-color: #338bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.next-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.next-btn:hover:not(:disabled) {
  background-color: #2a75d6;
}

.loading {
  color: white;
  font-size: 1.5rem;
}

@media (max-width: 600px) {
  .question-card {
    padding: 20px;
  }
}
</style>