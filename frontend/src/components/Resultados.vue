<template>
  <div class="results-container">
    <div class="results-card">
      <h2>Detalle de Respuestas</h2>

      <!-- Estado de carga o error -->
      <template v-if="loading">
        <p>Cargando resultados...</p>
      </template>
      <template v-else-if="error">
        <p class="error">{{ error }}</p>
      </template>

      <!-- Listado de preguntas con sus opciones y explicaciones -->
      <template v-else>
        <div class="inner-conainer">
          <div class="card-list">
            <div
              v-for="(q, index) in questions"
              :key="q.id"
              class="question-detail"
            >
              <h3>{{ index + 1 }}. {{ q.text }}</h3>
              <ul class="options-list">
                <li
                  v-for="opt in q.answer_options"
                  :key="opt.id"
                  :class="{ correct: opt.correct }"
                >
                  {{ opt.text }}
                  <span v-if="opt.correct">✔</span>
                </li>
              </ul>
              <p class="explanation">
                <strong>Explicación:</strong> {{ q.explanation }}
              </p>
            </div>
          </div>
        </div>  
        <button class="result-btn" @click="goHome">
          Volver al inicio
        </button>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'ResultsModal',
  setup() {
    const route = useRoute();
    const router = useRouter();

    // Flags y datos
    const loading = ref(true);
    const error = ref('');
    const questions = ref([]);

    // Obtenemos participationId y n desde query params
    const participationId = route.query.participationId;
    const totalQuestions = parseInt(route.query.n, 10);

    onMounted(async () => {
      if (!participationId || !totalQuestions) {
        error.value =
          'No se ha podido recuperar el identificador del test o el número de preguntas.';
        loading.value = false;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        for (let i = 1; i <= totalQuestions; i++) {
          const resp = await fetch(
            `http://${window.location.hostname}:8080/trivia/tests/${participationId}/question/${i}/`,
            {
              headers: {
                Accept: 'application/json',
                Authorization: `Token ${token}`,
              },
            }
          );
          if (!resp.ok) {
            throw new Error(
              `Error cargando pregunta ${i}: código ${resp.status}`
            );
          }
          const data = await resp.json();
          questions.value.push(data);
        }
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    });

    const goHome = () => {
      router.push({ name: 'MainForm' });
    };

    return {
      loading,
      error,
      questions,
      goHome,
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
  max-height: 100vh;
  background-image: url('@/assets/patron-move.gif');
  background-size: cover;
  background-repeat: no-repeat;
  padding: 20px;
  overflow: hidden;
}

.results-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 60%;
  max-width: 800px;
  text-align: left;
  /* Sin scroll en toda la tarjeta */
  overflow: visible;
  /* Altura máxima para dejar espacio al botón */
  max-height: 90vh;
}

.inner-conainer {
  /* Solo esta sección se desplaza */
  max-height: calc(90vh - 120px);
  overflow-y: auto;
  padding-right: 10px;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.question-detail {
  margin-bottom: 30px;
}

.options-list {
  list-style: none;
  padding: 0;
}

.options-list li {
  padding: 8px 12px;
  border-radius: 10px;
  margin-bottom: 8px;
  background-color: #f0f0f0;
}

.options-list li.correct {
  background-color: #05ab68;
  color: white;
}

.explanation {
  font-style: italic;
  margin-top: 8px;
}

.result-btn {
  display: block;
  margin: 20px auto 0;
  padding: 15px 30px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
}

.result-btn:hover {
  background-color: #52003b;
}

.error {
  color: #ff3333;
  font-size: 1.2rem;
  margin-bottom: 20px;
  text-align: center;
}
</style>