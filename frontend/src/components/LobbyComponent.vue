<template>
    <div class="lobby-screen">
      <h2 class="title">Modo Desafío</h2>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  
      <div v-if="!joined" class="lobby-actions">
        <!-- Sección de configuración de test -->
        <div class="config-panel">
          <h3>Seleccionar Categoría</h3>
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
          <p v-if="errorCategory" class="error">{{ errorCategory }}</p>
  
          <h3>Número de Preguntas</h3>
          <input
            type="number"
            v-model.number="numQuestions"
            min="1"
            class="questions-input"
            placeholder="Ingrese cantidad"
          />
          <p v-if="errorQuestions" class="error">{{ errorQuestions }}</p>
        </div>
  
        <button
          @click="createGame"
          :disabled="creating"
          class="btn-create"
        >
          {{ creating ? 'Creando...' : 'Crear nueva partida' }}
        </button>
  
        <p class="separator">O únete a una existente:</p>
  
        <!-- Sección lateral de partidas disponibles -->
        <ul v-if="!loading" class="games-list">
          <li v-for="game in games" :key="game.id" class="game-item">
            <span class="game-code">Código: {{ game.id }}</span>
            <button
              @click="joinExisting(game.id)"
              class="btn-join"
            >Unirse</button>
          </li>
        </ul>
        <p v-else class="loading-text">Cargando partidas...</p>
  
        <div class="join-custom">
          <input
            v-model="customId"
            placeholder="Ingrese código manual"
            class="input-code"
          />
          <button
            @click="joinExisting(customId)"
            :disabled="!customId"
            class="btn-join"
          >Unirse</button>
        </div>
      </div>
  
      <div v-else class="quiz-wrapper">
        <GameQuiz
          :test-id="String(selectedTestId)"
          @game-over="handleGameOver"
        />
      </div>
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
        errorCategory: '',
        errorQuestions: '',
        games: [],
        loading: false,
        creating: false,
        customId: '',
        selectedTestId: null,
        joined: false,
        errorMessage: ''
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
    methods: {
      async fetchCategories() {
        try {
          const token = localStorage.getItem('token');
          const res = await fetch(`http://${window.location.hostname}:8080/trivia/categories/`, {
            method: 'GET',
            headers: {
              accept: 'application/json',
              Authorization: `Token ${token}`
            }
          });
          if (res.ok) {
            this.categories = await res.json();
          }
        } catch {
            console.log("esto lobby coso")
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
          const response = await fetch(`http://${window.location.hostname}:8080/trivia/tests/available/`, {
            method: 'GET',
            headers: {
              accept: 'application/json',
              Authorization: `Token ${token}`
            }
          });
          if (response.ok) {
            this.games = await response.json();
          }
        } catch {
          this.errorMessage = 'Error de conexión al servidor.';
        } finally {
          this.loading = false;
        }
      },
      async createGame() {
        this.errorCategory = '';
        this.errorQuestions = '';
        if (!this.selectedCategory) {
          this.errorCategory = 'Seleccione una categoría.';
          return;
        }
        if (!this.numQuestions || this.numQuestions < 1) {
          this.errorQuestions = 'Ingrese un número válido de preguntas.';
          return;
        }
  
        this.creating = true;
        try {
          const token = localStorage.getItem('token');
          const payload = {
            n: this.numQuestions,
            category: this.selectedCategory.id
          };
          const response = await fetch(`http://${window.location.hostname}:8080/trivia/tests/multiplayer/create/`, {
            method: 'POST',
            headers: {
              accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Token ${token}`
            },
            body: JSON.stringify(payload)
          });
          if (response.ok) {
            const data = await response.json();
            this.games.push({ id: data.test_id });
            this.joinExisting(data.test_id);
          } else {
            // const errorText = await response.text();
            this.errorMessage = `Error al crear partida: ${response.status}`;
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
      handleGameOver(finalScore) {
        this.joined = false;
        this.selectedTestId = null;
        this.customId = '';
        this.fetchGames();
        this.$emit('game-ended', finalScore);
      }
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
  
  .lobby-screen {
      display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    background-image: url('@/assets/patron-move.gif');
    background-size: cover;
    background-position: center;  
  }
  
  .config-panel {
    background: #fff;
    padding: 1rem;
    border-radius: 8px;
  }
  .category-selection {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  .category-btn {
    background-color: #F9E8D9;
    color: #527853;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
  }
  .category-btn.selected {
    background-color: #527853;
    color: #fff;
  }
  .questions-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 6px;
  }
  
  .lobby-actions {
    grid-column: 1 / 2;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-create {
    background-color: #527853;
    color: white;
    padding: 0.75rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
  .separator {
    text-align: center;
    font-weight: bold;
    color: #333;
  }
  .games-list {
    list-style: none;
    padding: 0;
    max-height: 200px;
    overflow-y: auto;
  }
  .game-item {
    display: flex;
    justify-content: space-between;
    background: #F9E8D9;
    padding: 0.5rem;
    border-radius: 6px;
  }
  .btn-join {
    background-color: #527853;
    color: white;
    padding: 0.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  
  .join-custom {
    display: flex;
    gap: 0.5rem;
  }
  
  .quiz-wrapper {
    grid-column: 1 / -1;
  }
  
  .error {
    color: #ff3333;
  }
  
  .loading-text {
    font-style: italic;
    color: #333;
  }
  </style>