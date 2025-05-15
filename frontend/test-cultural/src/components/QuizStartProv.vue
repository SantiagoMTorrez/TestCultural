<template>
  <div class="quiz-container">
    <h2>Iniciando el cuestionario...</h2>
    <p v-if="!errorMessage">
      Estás a punto de comenzar un cuestionario de
      <strong>{{ category || 'la categoría seleccionada' }}</strong>
    </p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <button v-if="!errorMessage" @click="startQuiz">Comenzar Cuestionario</button>
    <button @click="goBack" class="back-btn">Volver</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'QuizStartProv',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const categoryId = ref('');
    const category = ref('');
    const loading = ref(false);
    const errorMessage = ref('');

    onMounted(async () => {
      console.log('QuizStartProv mounted, route query:', route.query);
      categoryId.value = route.query.categoryId || '';
      category.value = route.query.categoryName || '';

      // Guardar el ID de categoría en localStorage
      localStorage.setItem('idCategoria', categoryId.value);

      const token = localStorage.getItem('token');
      if (!token) {
        errorMessage.value = 'Debes iniciar sesión primero.';
        router.push('/login');
        return;
      }
      if (!categoryId.value) {
        errorMessage.value = 'No se especificó una categoría válida.';
        router.push('/mainform');
        return;
      }

      // Obtener todas las preguntas de la categoría
      loading.value = true;
      try {
        const response = await fetch(`http://localhost:8080/trivia/questions/?category=${categoryId.value}`, {
          headers: {
            accept: 'application/json',
            Authorization: `Token ${token}`,
          },
          method: 'GET',
        });

        if (response.ok) {
          const questions = await response.json();
          
          // Seleccionar 10 preguntas aleatorias
          const shuffled = questions.sort(() => 0.5 - Math.random());
          const selectedQuestions = shuffled.slice(0, 10).map(q => q.id);
          
          // Guardar en localStorage
          localStorage.setItem('preguntas', JSON.stringify(selectedQuestions));
          localStorage.setItem('puntero', '0');
          
          console.log('Preguntas seleccionadas:', selectedQuestions);
        } else {
          const errorText = await response.text();
          errorMessage.value = `Error al cargar preguntas: ${response.status}`;
          console.error('Error fetching questions:', response.status, errorText);
        }
      } catch (error) {
        console.error('Connection error:', error);
        errorMessage.value = 'Error de conexión al servidor.';
      } finally {
        loading.value = false;
      }
    });

    const startQuiz = () => {
      router.push('/quizGenericProv');
    };

    const goBack = () => {
      router.push('/mainform');
    };

    return { category, errorMessage, startQuiz, goBack };
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
  flex-direction: column;
  height: 100vh;
  /* background-image: url('@/assets/patrones.png'); */
  padding: 20px;
  text-align: center;
}

h2 {
  color: #161515;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #161515;
}

.error {
  color: #ff3333;
  font-size: 1.2rem;
  margin-bottom: 20px;
}

button {
  padding: 15px 30px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 10px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #52003b;
}

.back-btn {
  background-color: #ff3333;
}

.back-btn:hover {
  background-color: #cc0000;
}
</style>    