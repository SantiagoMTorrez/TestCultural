<template>
  <div class="quiz-container">
    <h2>Iniciando el cuestionario...</h2>
    <p v-if="!errorMessage">
      Estás a punto de comenzar un cuestionario de
      <strong>{{ category || 'la categoría seleccionada' }}</strong>
      con dificultad
      <strong>{{ difficulty || 'Fácil' }}</strong>.
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
  name: 'QuizStart',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const categoryId = ref('');
    const category = ref('');
    const difficulty = ref('');
    const loading = ref(false);
    const errorMessage = ref('');

    onMounted(async () => {
      console.log('QuizStart mounted, route query:', route.query);
      categoryId.value = route.query.categoryId || '';
      category.value = route.query.categoryName || '';
      difficulty.value = route.query.difficulty || 'Fácil';

      const token = localStorage.getItem('token');
      console.log('Token:', token ? token : 'Missing');
      if (!token) {
        console.error('No token found');
        errorMessage.value = 'Debes iniciar sesión primero.';
        router.push('/login');
        return;
      }
      if (!categoryId.value) {
        console.error('No categoryId provided');
        errorMessage.value = 'No se especificó una categoría válida.';
        router.push('/mainform');
        return;
      }

      if (categoryId.value && !category.value) {
        console.log('Fetching category name for categoryId:', categoryId.value);
        loading.value = true;
        try {
          const response = await fetch(`http://localhost:8080/trivia/categories/${categoryId.value}/`, {
            headers: {
              accept: 'application/json',
              Authorization: `Token ${token}`,
            },
            method: 'GET',
          });
          console.log('Category fetch response status:', response.status);
          if (response.ok) {
            const data = await response.json();
            category.value = data.name || 'Categoría';
            console.log('Category name fetched:', category.value);
          } else {
            const errorText = await response.text();
            console.error('Error fetching category:', response.status, errorText);
            errorMessage.value = `No se pudo cargar la categoría: ${response.status} ${errorText}`;
          }
        } catch (error) {
          console.error('Connection error fetching category:', error);
          errorMessage.value = 'Error de conexión al servidor.';
        } finally {
          loading.value = false;
        }
      }
    });

    const startQuiz = () => {
      console.log('Starting quiz with:', {
        categoryId: categoryId.value,
        categoryName: category.value,
        difficulty: difficulty.value,
      });
      router.push({
        path: '/quiz',
        query: {
          categoryId: categoryId.value,
          categoryName: category.value,
          difficulty: difficulty.value,
        },
      });
    };

    const goBack = () => {
      console.log('Returning to mainform');
      router.push('/mainform');
    };

    return { router, category, difficulty, loading, errorMessage, startQuiz, goBack };
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
  background-image: url('@/assets/patrones.png');
  padding: 20px;
  text-align: center;
}

h2 {
  color: #ececec;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #ececec;
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
