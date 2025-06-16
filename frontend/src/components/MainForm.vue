<template>
  <div class="page-wrapper">
    <header class="site-header">
      <div class="header-content">
        <nav class="nav-actions">
          <button class="nav-btn challenge" @click="selectMode('Desafío')">Desafío</button>
          <button class="nav-btn educational" @click="modoEducativo">Educativo</button>
          <button class="nav-btn ranking" @click="selectMode('Ranking')">Ranking</button>
        </nav>
      </div>
    </header>

    <section class="hero">
      <div class="hero-overlay">
        <h1 class="hero-title">Trivia Bolivia</h1>
      </div>
    </section>

    <main class="main-container">
      <aside class="user-panel">
        <div class="avatar-wrapper">
          <img src="@/assets/avatar.png" alt="Avatar" class="avatar" />
          <p class="user-name">{{ userName }}</p>
        </div>
        <button @click="logout" class="logout-btn">Cerrar sesión</button>
      </aside>

      <section class="form-box">
        <h2 class="section-title">Crear Prueba</h2>

        <div class="category-selection">
          <button
            v-for="category in categories"
            :key="category.id"
            class="category-btn"
            :class="{ selected: selectedCategory?.id === category.id }"
            @click="selectCategory(category)"
          >
            {{ category.name }}
          </button>
        </div>

        <div class="form-group">
          <label>Elegir Dificultad</label>
          <select v-model="selectedDifficulty" class="input-control">
            <option value="Fácil">Fácil</option>
            <option value="Medio">Medio</option>
            <option value="Difícil">Difícil</option>
          </select>
        </div>

        <div class="form-group">
          <label>Número de preguntas</label>
          <input
            type="number"
            v-model.number="numQuestions"
            min="1"
            placeholder="10"
            class="input-control"
          />
          <p v-if="errorQuestions" class="form-error">{{ errorQuestions }}</p>
        </div>

        <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>
        <button @click="startQuiz" class="start-btn" :disabled="!!errorMessage || !!errorQuestions">
          ¡VAMOS!
        </button>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'MainForm',
  setup() {
    const router = useRouter();
    const userName = ref('');
    const categories = ref([]);
    const selectedCategory = ref(null);
    const selectedDifficulty = ref('Fácil');
    const numQuestions = ref(10);
    const errorMessage = ref('');
    const errorQuestions = ref('');

    onMounted(async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        errorMessage.value = 'Debes iniciar sesión primero.';
        setTimeout(() => router.push('/login'), 2000);
        return;
      }

      userName.value = localStorage.getItem('dataname') || 'Usuario';

      try {
        const res = await fetch(`http://${window.location.hostname}:8080/trivia/categories/`, {
          headers: { accept: 'application/json', Authorization: `Token ${token}` },
          method: 'GET',
        });
        if (res.ok) categories.value = await res.json();
        else {
          const txt = await res.text();
          errorMessage.value = `Error ${res.status}: ${txt}`;
          if (res.status === 401) setTimeout(() => router.push('/login'), 2000);
        }
      } catch {
        errorMessage.value = 'No se pudo conectar al servidor.';
      }
    });

    const selectCategory = (cat) => (selectedCategory.value = cat);
    const selectMode = (mode) => router.push(mode === 'Ranking' ? '/player-ranking' : '/lobby');
    const modoEducativo = () => router.push('/modoEducativo');

    const startQuiz = () => {
      errorQuestions.value = '';
      if (!selectedCategory.value) { errorMessage.value = 'Selecciona una categoría.'; return; }
      if (numQuestions.value < 1) { errorQuestions.value = 'Debe ser >= 1.'; return; }

      router.push({ path: '/quizstart', query: {
        categoryId: selectedCategory.value.id,
        categoryName: selectedCategory.value.name,
        difficulty: selectedDifficulty.value,
        n: numQuestions.value,
      }});
    };

    const logout = () => { localStorage.clear(); router.push('/login'); };

    return { userName, categories, selectedCategory, selectedDifficulty, numQuestions,
      errorMessage, errorQuestions, selectCategory, selectMode, modoEducativo, startQuiz, logout };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend+Giga&display=swap');

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
</style>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-image: url('@/assets/patron-move.gif');
  background-size: cover;
  background-position: center;
}

.site-header {
  background: #000;
  color: #fff;
  box-shadow: var(--shadow);
}
.header-content {
  max-width: 1200px;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
}

.nav-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.nav-btn { background: transparent; border: none; padding: 0.5rem 1rem; border-radius: var(--radius); cursor: pointer; color: #fff; transition: background 0.3s; }
.nav-btn:hover { background: var(--c-secondary); }

.hero {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-overlay {
  background: rgba(0,0,0,0.4);
  padding: 1rem 2rem;
  border-radius: var(--radius);
}
.hero-title { color: #fff; font-size: 2rem; font-weight: 200; }

.main-container {
  background: var(--c-panel);
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: -80px auto 2rem;
  padding: 0 1rem;
  border-radius: var(--radius);
  z-index: 10;
}

.user-panel { background: var(--c-panel); border-radius: var(--radius); box-shadow: var(--shadow); padding: 1rem; text-align: center; }
.avatar { width: 80px; height: 80px; border-radius: 50%; margin-bottom: 0.5rem; }
.user-name { font-weight: bold; }
.logout-btn { background: var(--c-error); padding: 0.5rem 1rem; border: none; border-radius: var(--radius); color: #fff; cursor: pointer; }
.logout-btn:hover { background: #a62828; }

.form-box { padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem; }
.section-title { font-size: 1.4rem; border-left: 4px solid var(--c-primary); padding-left: 0.5rem; margin-bottom: 1rem; }
.category-selection { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.category-btn { padding: 0.5rem 1rem; border: 1px solid var(--c-primary); border-radius: var(--radius); background: transparent; cursor: pointer; }
.category-btn.selected { background: var(--c-primary); color: #fff; }
.category-btn:hover:not(.selected) { background: var(--c-secondary); color: #fff; }

.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.input-control { padding: 0.6rem 1rem; border: 1px solid #ccc; border-radius: var(--radius); }
.form-error { color: var(--c-error); }
.start-btn { align-self: flex-start; padding: 0.75rem 2rem; background: var(--c-primary); color: #fff; border: none; border-radius: var(--radius); cursor: pointer; }
.start-btn:disabled { background: #ccc; cursor: not-allowed; }
.start-btn:hover:not(:disabled) { background: var(--c-secondary); }

/* Responsive Breakpoints */
@media (max-width: 1024px) {
  .main-container { display: block; margin: -40px 1rem 2rem; padding: 1rem; }
  .user-panel { margin-bottom: 1rem; }
  .form-box { padding: 1rem; }
}
@media (max-width: 600px) {
  .hero { height: 150px; }
  .hero-title { font-size: 1.5rem; }
  .nav-actions { justify-content: center; }
  .header-content { flex-direction: column; }
  .section-title { font-size: 1.2rem; }
  .category-btn { font-size: 0.9rem; padding: 0.4rem 0.8rem; }
  .input-control { font-size: 0.9rem; padding: 0.5rem; }
  .start-btn { width: 100%; padding: 0.6rem; }
}
</style>