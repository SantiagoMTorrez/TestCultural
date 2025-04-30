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
          <button class="mode-btn challenge" @click="selectMode('Desafío')">Modo Desafío</button>
          <button class="mode-btn educational" @click="selectMode('Educativo')">Modo Educativo</button>
          <button class="mode-btn ranking" @click="selectMode('Ranking')">Ver Ranking</button>
        </div>
  
        <!-- Título y espacio -->
        <h3 class="title">Seleccionar Prueba</h3>
  
        <!-- Selección de categoría -->
        <div class="category-selection">
          <button v-for="category in categories" :key="category" class="category-btn" @click="selectCategory(category)">
            {{ category }}
          </button>
        </div>
  
        <!-- Selección de dificultad -->
        <h3>Elegir Dificultad</h3>
        <select v-model="selectedDifficulty" class="difficulty-select">
          <option value="Fácil">Fácil</option>
          <option value="Medio">Medio</option>
          <option value="Difícil">Difícil</option>
          <option value="Intenso">Intenso</option>
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
    name: "MainForm",
    setup() {
      const router = useRouter();
      const userName = ref('');
      const categories = ['Historia', 'Arte', 'Literatura', 'Gastronomía', 'Tradiciones'];
      const selectedCategory = ref('Arte');
      const selectedDifficulty = ref('Fácil');
  
      onMounted(() => {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Debes iniciar sesión primero.');
          router.push('/');
          return;
        }
  
        const name = localStorage.getItem('dataname');
        userName.value = name || 'Usuario';
      });
  
      const selectCategory = (category) => {
        selectedCategory.value = category;
      };
  
      const selectMode = (mode) => {
        console.log(`Modo seleccionado: ${mode}`);
      };
  
      const startQuiz = () => {
        console.log(`Iniciando el cuestionario con categoría: ${selectedCategory.value} y dificultad: ${selectedDifficulty.value}`);
        router.push('/quiz');
      };

      const logout = () => {
        localStorage.removeItem('token');
        router.push('/');
      };
  
      return { userName, categories, selectedCategory, selectedDifficulty, selectCategory, selectMode, startQuiz, logout };
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
  
  * {
    font-family: 'Jeju Hallasan', cursive;
  }
  
  .main-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('@/assets/patrones.png');
    background-size: cover;
  }
  
  .form-box {
    background: rgba(255, 255, 255, 0.95);
    padding: 3rem 2rem;
    border-radius: 20px;
    box-shadow: 0 0 15px #00000055;
    text-align: center;
    max-width: 700px;
    width: 100%;
    position: relative;  /* Para posicionar los elementos en el contenedor */
  }
  
  .header-left, .header-right {
    position: absolute;
    top: 20px;
  }
  
  .header-left {
    left: 20px;  /* Alinea al borde superior izquierdo */
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .header-right {
    right: 20px; /* Alinea al borde superior derecho */
    display: flex;
    gap: 15px;
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
  }
  
  .mode-btn {
    padding: 12px 24px;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: background-color 0.3s;
    width: 120px;  /* Ancho fijo para los botones */
  }
  
  .mode-btn.challenge {
    background-color: #ff3333; /* Rojo cálido para Desafío */
  }
  
  .mode-btn.educational {
    background-color: #05ab68; /* Naranja para Educativo */
  }
  
  .mode-btn.ranking {
    background-color: #338bff; /* Naranja claro para Ranking */
  }
  
  .mode-btn:hover {
    background-color: #7c716d; /* Rojo más oscuro al pasar el mouse */
  }
  
  .category-selection {
    display: flex;
    justify-content: space-around;
    margin-top: 50px;  /* Mayor espacio entre los botones de modo y el título */
    margin-bottom: 20px;
  }
  
  .category-btn {
    padding: 12px 20px;
    background-color: #008CBA; /* Azul para las categorías */
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background-color 0.3s;
  }

  
  .category-btn:hover {
    background-color: #4e6267; /* Azul oscuro al pasar el mouse */
  }
  
  .difficulty-select {
    padding: 12px;
    margin-top: 20px;
    font-size: 1.1rem;
    background-color: #e3dbdc; /* Rosa para el selector de dificultad */
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  
  .title {
    font-size: 1.8rem;
    margin-top: 60px; /* Más espacio antes del título */
    margin-bottom: 20px;
  }
  
  .start-btn {
    padding: 16px 35px;
    background-color: #6D004D;  /* Rojo profundo para el botón "¡VAMOS!" */
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1.3rem;
    cursor: pointer;
    margin-top: 20px;
    transition: background-color 0.3s;
  }
  
  .start-btn:hover {
    background-color: #52003B; /* Color oscuro al pasar el mouse */
  }

  .logout-btn {
    padding: 12px 25px;
    background-color: #ff3333; /* Rojo cálido para Cerrar Sesión */
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Jeju Hallasan', cursive;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background-color 0.3s;
    margin-top: 20px; /* Espacio entre el botón de inicio y el de cerrar sesión */
  }

  .logout-btn-left {
    position: absolute;
    bottom: 20px; /* Alinea al borde inferior */
    left: 20px;   /* Alinea al borde izquierdo */
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .logout-btn:hover {
    background-color: #7c716d; /* Rojo más oscuro al pasar el mouse */
  }
  </style>
  