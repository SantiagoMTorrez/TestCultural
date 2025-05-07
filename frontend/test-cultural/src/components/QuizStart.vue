<template>
  <div class="quiz-container">
    <h2>Iniciando el cuestionario...</h2>
    <p>En breve verás las preguntas del cuestionario basado en la categoría y dificultad seleccionadas.</p>
    <button @click="startQuiz">Comenzar Cuestionario</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  methods: {
    startQuiz() {
      console.log('Comenzando el cuestionario...');
      if (this.category === 'Historia') {
        this.router.push({
          path: '/quizHistoria',
          query: { difficulty: this.difficulty }
        });
        return;
      }
      alert('El cuestionario para esta categoría no está disponible.');
    }
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const questions = ref([]);
    const category = ref('');
    const difficulty = ref('');
    const loading = ref(true);

    onMounted(async () => {
      // Get query parameters
      category.value = route.query.category || '';
      difficulty.value = route.query.difficulty || 'Fácil';

      // Fetch questions for all categories (including Historia, as a fallback)
      try {
        const response = await fetch(
          `http://localhost:8080/trivia/questions/?category=${encodeURIComponent(category.value)}&difficulty=${encodeURIComponent(difficulty.value)}`,
          {
            headers: {
              "accept": "application/json",
              'Authorization': `Token ${localStorage.getItem('token')}`
            },
            method: "GET"
          }
        );

        if (response.ok) {
          questions.value = await response.json();
        } else {
          console.error("Error al obtener preguntas");
          alert("No se pudieron cargar las preguntas.");
        }
      } catch (error) {
        console.error("Error de conexión:", error);
        alert("Error al conectar con el servidor.");
      } finally {
        loading.value = false;
      }
    });

    return { router, questions, category, difficulty, loading };
  }
};
</script>

<style scoped>
.quiz-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

button {
  padding: 15px 30px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
}

button:hover {
  background-color: #52003b;
}
</style>