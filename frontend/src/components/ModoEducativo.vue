<template>
  <div class="educational-container">
    <div class="panel">
      <h2 class="panel-title">Modo Educativo</h2>

      <div class="scroll-container">
        <div class="questions-grid">
          <div
            v-for="question in questions"
            :key="question.id"
            class="transform-wrapper"
          >
            <div class="card front">
              <div class="card-header">
                <strong>{{ question.text }}</strong>
              </div>
              <div class="card-footer">
                <span
                  class="difficulty-badge"
                  :class="getDifficultyClass(question.difficulty)"
                >
                  {{ getDificultadText(question.difficulty) }}
                </span>
              </div>
            </div>

            <div class="card back">
              <div class="card-content">
                {{ question.explanation || 'Esta pregunta no tiene explicación' }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="btn-secondary exit-btn" @click="salir">Salir</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'ModoEducativo',
  setup() {
    const router = useRouter();
    const questions = ref([]);

    const getDificultadText = (difficulty) => {
      switch (difficulty) {
        case 1:
          return 'Fácil';
        case 2:
          return 'Media';
        case 3:
          return 'Difícil';
        default:
          return 'Desconocida';
      }
    };

    const getDifficultyClass = (difficulty) => {
      switch (difficulty) {
        case 1:
          return 'easy';
        case 2:
          return 'medium';
        case 3:
          return 'hard';
        default:
          return 'unknown';
      }
    };

    const cargarPreguntas = async () => {
      try {
        const res = await fetch(
          `http://${window.location.hostname}:8080/trivia/questions/`,
          {
            method: 'GET',
            headers: {
              accept: 'application/json',
              Authorization: `Token ${localStorage.getItem('token')}`,
            },
          }
        );
        if (res.ok) questions.value = await res.json();
      } catch (e) {
        console.error('Error de conexión:', e);
      }
    };

    onMounted(cargarPreguntas);

    const salir = () => {
      router.push('/mainform');
    };

    return {
      questions,
      getDificultadText,
      getDifficultyClass,
      salir,
    };
  },
};
</script>

<style>
/* Global styles and variables */
@import url('https://fonts.googleapis.com/css2?family=Lexend+Giga:wght@400;600&display=swap');

:root {
  --font-base: 'Lexend Giga', sans-serif;
  --c-bg: #fafafa;
  --c-panel: #ffffff;
  --c-text: #333333;
  --c-primary: #004d40;
  --c-secondary: #00796b;
  --c-error: #c62828;
  --radius: 12px;
  --shadow: 0 4px 16px rgba(0,0,0,0.08);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: var(--font-base);
  color: var(--c-text);
}

body {
  background: var(--c-bg);
}
</style>

<style scoped>
.educational-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: black;
  background-image: url('@/assets/patron-move.gif');
  background-size: cover;
  background-repeat: no-repeat;
}

.panel {
  background: #BBB;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--c-primary);
  text-align: center;
}

.scroll-container {
  overflow: auto;
  flex-grow: 1;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.transform-wrapper {
  perspective: 600px;
  position: relative;
  height: 200px;
}

.card {
  position: absolute;
  width: 100%;
  height: 100%;
  background: var(--c-panel);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  backface-visibility: hidden;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.front {
  transform: rotateY(0deg);
}

.back {
  transform: rotateY(-180deg);
}

.transform-wrapper:hover .front {
  transform: rotateY(180deg);
}

.transform-wrapper:hover .back {
  transform: rotateY(0deg);
}

.card-header {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.card-content {
  flex-grow: 1;
  margin: 0.5rem 0;
  line-height: 1.4;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.difficulty-badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.8rem;
  color: #fff;
}

.difficulty-badge.easy {
  background: #4caf50;
}

.difficulty-badge.medium {
  background: #ffc107;
}

.difficulty-badge.hard {
  background: #f44336;
}

.difficulty-badge.unknown {
  background: #9e9e9e;
}

.exit-btn {
  align-self: center;
  padding: 0.75rem 1.5rem;
  background: var(--c-secondary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.exit-btn:hover {
  background: var(--c-primary);
}

@media (max-width: 768px) {
  .questions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
