<template>
  <div class="lobby-screen">
    <header class="lobby-header">
      <h2 class="lobby-title">Modo Desafío</h2>
    </header>

    <section v-if="!joined" class="lobby-container">
      <aside class="config-panel">
        <h3 class="section-title">Configuración</h3>

        <div class="form-group">
          <label>Seleccionar Categoría</label>
          <div class="category-selection">
            <button
              v-for="cat in categories"
              :key="cat.id"
              class="category-btn"
              :class="{ selected: selectedCategory && selectedCategory.id === cat.id }"
              @click="selectCategory(cat)"
            >
              {{ cat.name }}
            </button>
          </div>
          <p v-if="errorCategory" class="form-error">{{ errorCategory }}</p>
        </div>

        <div class="form-group">
          <label>Número de Preguntas</label>
          <input
            type="number"
            v-model.number="numQuestions"
            min="1"
            step="1"
            class="input-control"
            placeholder="5"
          />
        </div>

        <div class="form-group">
          <label>Tiempo Límite (min)</label>
          <input
            type="number"
            v-model.number="timeLimit"
            min="1"
            max="120"
            step="1"
            class="input-control"
            placeholder="10"
          />
          <p v-if="errorQuestions" class="form-error">{{ errorQuestions }}</p>
        </div>

        <div class="actions">
          <button
            @click="createGame"
            :disabled="creating"
            class="btn-primary"
          >
            {{ creating ? 'Creando...' : 'Crear Partida' }}
          </button>
        </div>

        <p class="separator">O únete a una existente</p>

        <ul v-if="!loading" class="games-list">
          <li v-for="game in games" :key="game.id" class="game-item">
            <span class="game-code">Código: {{ game.id }}</span>
            <button
              @click="joinExisting(game.id)"
              class="btn-secondary"
            >
              Unirse
            </button>
          </li>
        </ul>
        <p v-else class="loading-text">Cargando partidas...</p>

        <div class="join-custom">
          <input
            v-model="customId"
            placeholder="Código manual"
            class="input-control"
          />
          <button
            @click="joinExisting(customId)"
            :disabled="!customId"
            class="btn-secondary"
          >
            Unirse
          </button>
        </div>
      </aside>

      <div class="lobby-error" v-if="errorMessage">
        <p class="form-error">{{ errorMessage }}</p>
      </div>
    </section>

    <section v-else class="quiz-wrapper">
      <GameQuiz
        :test-id="String(selectedTestId)"
        @game-over="handleGameOver"
      />
    </section>
  </div>
</template>

<script>
import GameQuiz from '@/components/GameQuiz.vue';
export default {
  name: 'LobbyComponent',
  components: { GameQuiz },
  data() {
    return {
      categories: [],
      selectedCategory: null,
      numQuestions: 5,
      timeLimit: 10,
      errorCategory: '',
      errorQuestions: '',
      games: [],
      loading: false,
      creating: false,
      customId: '',
      selectedTestId: null,
      joined: false,
      errorMessage: '',
      gamesTimeoutCallback: null,
    };
  },
  async mounted() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.errorMessage = 'Debes iniciar sesión primero.';
      setTimeout(() => this.$router.push('/login'), 2000);
      return;
    }
    await Promise.all([this.fetchCategories(), this.fetchGames()]);
  },
  beforeUnmount() {
    clearTimeout(this.gamesTimeoutCallback);
  },
  methods: {
    async fetchCategories() {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://${window.location.hostname}:8080/trivia/categories/`, {
          method: 'GET',
          headers: { accept: 'application/json', Authorization: `Token ${token}` }
        });
        if (res.ok) this.categories = await res.json();
      } catch {
        console.log("what")
      }
    },
    selectCategory(cat) {
      this.selectedCategory = cat;
      this.errorCategory = '';
    },
    async fetchGames() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://${window.location.hostname}:8080/trivia/tests/available/`, {
          method: 'GET',
          headers: { accept: 'application/json', Authorization: `Token ${token}` }
        });
        if (res.ok) this.games = await res.json();
      } catch {
        this.errorMessage = 'Error de conexión al servidor.';
      } finally {
        this.loading = false;
      }
      this.gamesTimeoutCallback = setTimeout(this.fetchGames, 5000);
    },
    async createGame() {
      this.errorCategory = '';
      this.errorQuestions = '';
      if (!this.selectedCategory) {
        this.errorCategory = 'Seleccione una categoría.';
        return;
      }
      if (this.numQuestions < 1) {
        this.errorQuestions = 'Número de preguntas inválido.';
        return;
      }
      this.creating = true;
      try {
        const token = localStorage.getItem('token');
        const payload = { n: this.numQuestions, category: this.selectedCategory.id, time_limit_minutes: this.timeLimit };
        const res = await fetch(`http://${window.location.hostname}:8080/trivia/tests/multiplayer/create/`, {
          method: 'POST', headers: { accept: 'application/json', 'Content-Type': 'application/json', Authorization: `Token ${token}` },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          const data = await res.json();
          this.joinExisting(data.test_id);
        } else {
          this.errorMessage = `Error ${res.status} al crear partida.`;
        }
      } catch {
        this.errorMessage = 'Error de conexión al crear partida.';
      } finally {
        this.creating = false;
      }
    },
    joinExisting(id) {
      this.selectedTestId = id;
      this.joined = true;
    },
    handleGameOver(score) {
      this.joined = false;
      this.selectedTestId = null;
      this.customId = '';
      this.fetchGames();
      this.$emit('game-ended', score);
    }
  }
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
.lobby-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: black;
  min-height: 100vh;
  padding: 2rem;

  background-size: cover;
  background-repeat: no-repeat;
  background-image: url('@/assets/patron-move.gif');

}

.lobby-header {
  width: 100%;
  background: var(--c-primary);
  padding: 1rem;
  box-shadow: var(--shadow);
}

.lobby-title {
  color: #fff;
  text-align: center;
  font-size: 1.5rem;
}

.lobby-container {
  display: flex;
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  margin-top: 2rem;
}

.config-panel {
  background: var(--c-panel);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  flex: 1;
}

.section-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  border-left: 4px solid var(--c-primary);
  padding-left: 0.5rem;
}

.category-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.category-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--c-primary);
  border-radius: var(--radius);
  background: transparent;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.category-btn.selected {
  background: var(--c-primary);
  color: #fff;
}

.input-control {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: var(--radius);
  font-size: 1rem;
}

.actions {
  margin-top: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary {
  background: var(--c-primary);
  color: #fff;
}

.btn-primary:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  background: var(--c-secondary);
}

.btn-secondary {
  background: var(--c-secondary);
  color: #fff;
}

.games-list {
  list-style: none;
  padding: 0;
  flex: 1;
  max-height: 300px;
  overflow-y: auto;
}

.game-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--c-panel);
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.join-custom {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.loading-text,
.lobby-error .form-error {
  text-align: center;
  color: var(--c-error);
  margin-top: 1rem;
}
</style>
