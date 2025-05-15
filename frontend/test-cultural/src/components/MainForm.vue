<template>
  <div class="main-container">
    <div class="form-box">
      <!-- Encabezado con foto y nombre del usuario alineado a la izquierda -->
      <div class="header-left">
        <img src="@/assets/avatar.png" alt="Avatar" class="avatar" />
        <div class="user-info">
          <p>{{ userName }}</p>
        </div>
      </div>

      <!-- Botones de modo y ranking alineados a la derecha -->
      <div class="header-right">
        <button class="mode-btn challenge" @click="selectMode('Desafío')">Modo Desafio</button>
        <button class="mode-btn educational" @click="selectMode('Educativo')">Modo Educativo</button>
        <button class="mode-btn ranking" @click="selectMode('Ranking')">Ver Ranking</button>
      </div>

      <!-- Título y espacio -->
      <h3 class="title">Seleccionar Prueba</h3>

      <!-- Selección de categoría -->
      <div class="category-selection">
        <button
          v-for="category in categories"
          :key="category.id"
          class="category-btn"
          :class="{ 'selected': selectedCategory?.id === category.id }"
          @click="selectCategory(category)"
        >
          {{ category.name }}
        </button>
      </div>

      <!-- Selección de dificultad -->
      <h3>Elegir Dificultad</h3>
      <select v-model="selectedDifficulty" class="difficulty-select">
        <option value="Fácil">Fácil</option>
        <option value="Medio">Medio</option>
        <option value="Difícil">Difícil</option>
      </select>

      <!-- Botón para iniciar -->
      <button @click="startQuiz" class="start-btn">¡VAMOS!</button>
    </div>
    <button @click="logout" class="logout-btn">CERRAR SESIÓN</button>
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

    onMounted(async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Debes iniciar sesión primero.');
        router.push('/');
        return;
      }

      userName.value = localStorage.getItem('dataname') || 'Usuario';

      try {
        const response = await fetch('http://localhost:8080/trivia/categories/', {
          headers: {
            accept: 'application/json',
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
          method: 'GET',
        });

        if (response.ok) {
          categories.value = await response.json();
        } else {
          console.error('Error al obtener categorías');
          alert('No se pudieron cargar las categorías.');
        }
      } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error de conexión al servidor.');
      }
    });

    const selectCategory = (category) => {
      selectedCategory.value = category;
    };

    const selectMode = (mode) => {
      if (mode === 'Educativo') {
        router.push('/modoEducativo');
      } else {
        console.log(`Modo seleccionado: ${mode}`);
        // Lógica para otros modos si es necesario
      }
    };

    const startQuiz = () => {
      if (!selectedCategory.value) {
        alert('Por favor, selecciona una categoría.');
        return;
      }
      router.push({
        path: '/quiz',
        query: {
          categoryId: selectedCategory.value.id,
          categoryName: selectedCategory.value.name,
          difficulty: selectedDifficulty.value,
        },
      });
    };

    const logout = () => {
      localStorage.removeItem('token');
      router.push('/');
    };

    return { 
      userName, 
      categories, 
      selectedCategory, 
      selectedDifficulty, 
      selectCategory, 
      selectMode, 
      startQuiz, 
      logout 
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
  box-sizing: border-box;
}

.main-container {
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

.form-box {
  background: rgba(255, 255, 255, 0.95);
  padding: 3rem 2rem;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 700px;
  width: 100%;
  position: relative;
  animation: fadeIn 1s ease-in-out;
}

.header-left,
.header-right {
  position: absolute;
  top: 20px;
}

.header-left {
  left: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  right: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ddd;
}

.user-info p {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0;
}

.mode-btn {
  padding: 10px 20px;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  width: 110px;
}

.mode-btn.challenge {
  background-color: #ff3333;
}

.mode-btn.educational {
  background-color: #05ab68;
}

.mode-btn.ranking {
  background-color: #338bff;
}

.mode-btn:hover {
  background-color: #7c716d;
}

.title {
  font-size: 1.8rem;
  margin-top: 70px;
  margin-bottom: 20px;
}

.category-selection {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-around;
  margin-bottom: 20px;
  width: 100%;
  overflow-x: auto;
}

.category-btn {
  padding: 12px 20px;
  margin: 5px;
  background-color: #008CBA;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.category-btn:hover {
  background-color: #4e6267;
}

.difficulty-select {
  padding: 12px;
  margin-top: 10px;
  font-size: 1.1rem;
  background-color: #e3dbdc;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 70%;
}

.start-btn {
  padding: 16px 35px;
  background-color: #6D004D;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.3rem;
  cursor: pointer;
  margin-top: 25px;
  transition: background-color 0.3s;
}

.start-btn:hover {
  background-color: #52003B;
}

.logout-btn {
  margin-top: 30px;
  background-color: #ff3333;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 10px;
  font-size: 1.2rem;
  font-family: 'Jeju Hallasan', cursive;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #7c716d;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>