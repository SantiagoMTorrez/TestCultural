<template>
    <transition name="fade-slide-up">
      <div class="main-container">
        <div class="form-box">
          <!-- Encabezado con foto y nombre del usuario -->
          <div class="header-left">
            <img src="@/assets/avatar.png" alt="Avatar" class="avatar" />
            <div class="user-info">
              <p>{{ userName }}</p>
            </div>
          </div>
  
          <h3 class="title">Panel de Staff</h3>
  
          <!-- Botones -->
          <div class="button-container">
            <button class="action-btn new-category" @click="nuevaCategoria">
              Nueva Categoría
            </button>
            <button class="action-btn new-question" @click="nuevaPregunta">
              Nueva Pregunta
            </button>
          </div>
        </div>
  
        <!-- Cerrar sesión -->
        <button @click="logout" class="logout-btn">CERRAR SESIÓN</button>
      </div>
    </transition>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: "StaffMain",
    setup() {
      const router = useRouter();
      const userName = ref('');
  
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
  
      const nuevaCategoria = () => {
        router.push('/nuevaCategoria');
      };
  
      const nuevaPregunta = () => {
        router.push('/nuevaPreguntas');
      };
  
      const logout = () => {
        localStorage.removeItem('token');
        router.push('/');
      };
  
      return { userName, nuevaCategoria, nuevaPregunta, logout };
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
    background-image: url('@/assets/patron-move.gif');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    padding: 1rem;
  }
  
  .form-box {
    background: #F9E8D9;
    padding: 3rem 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    text-align: center;
    max-width: 700px;
    width: 100%;
    position: relative;
  }
  
  .header-left {
    position: absolute;
    top: 20px;
    left: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #EEE;
    border: 2px solid #527853;
  }
  
  .user-info p {
    font-size: 1.2rem;
    font-weight: bold;
    color: #527853;
  }
  
  .title {
    font-size: 2rem;
    margin-top: 60px;
    margin-bottom: 40px;
    color: #EE7214;
  }
  
  .button-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    align-items: center;
  }
  
  .action-btn {
    padding: 16px 35px;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1.2rem;
    cursor: pointer;
    width: 250px;
    transition: transform 0.2s, background-color 0.3s;
  }
  
  .action-btn:hover {
    transform: scale(1.05);
  }
  
  .action-btn.new-category {
    background-color: #527853;
  }
  
  .action-btn.new-question {
    background-color: #F7B787;
    color: #333;
  }
  
  .logout-btn {
    margin-top: 30px;
    padding: 12px 25px;
    background-color: #EE7214;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background-color 0.3s, transform 0.2s;
  }
  
  .logout-btn:hover {
    background-color: #C25C0C;
    transform: scale(1.05);
  }
  
  /* Animación suave al cargar */
  .fade-slide-up-enter-active {
    transition: all 0.8s ease;
  }
  
  .fade-slide-up-enter-from {
    opacity: 0;
    transform: translateY(30px);
  }
  </style>
  