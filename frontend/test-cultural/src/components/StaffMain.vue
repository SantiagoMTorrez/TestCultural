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
  
        <!-- Título -->
        <h3 class="title">Panel de Staff</h3>
  
        <!-- Botones centrales -->
        <div class="button-container">
          <button class="action-btn new-category" @click="nuevaCategoria">
            Nueva Categoría
          </button>
          <button class="action-btn new-question" @click="nuevaPregunta">
            Nueva Pregunta
          </button>
        </div>
      </div>
      <button @click="logout" class="logout-btn">CERRAR SESIÓN</button>
    </div>
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
        console.log('Nueva categoría');
        router.push('/nuevaCategoria');
        // Aquí iría la lógica para crear nueva categoría
      };
  
      const nuevaPregunta = () => {
        console.log('Nueva pregunta');
        router.push('/nuevaPreguntas');
        // Aquí iría la lógica para crear nueva pregunta
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
    background-color: #ddd;
  }
  
  .user-info p {
    font-size: 1.2rem;
    font-weight: bold;
  }
  
  .title {
    font-size: 1.8rem;
    margin-top: 20px;
    margin-bottom: 50px;
  }
  
  .button-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
    align-items: center;
    margin-top: 30px;
  }
  
  .action-btn {
    padding: 16px 35px;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1.3rem;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 250px;
  }
  
  .action-btn.new-category {
    background-color: #05ab68; /* Verde para Nueva Categoría */
  }
  
  .action-btn.new-question {
    background-color: #338bff; /* Azul para Nueva Pregunta */
  }
  
  .action-btn:hover {
    background-color: #7c716d; /* Color oscuro al pasar el mouse */
  }
  
  .logout-btn {
    padding: 12px 25px;
    background-color: #ff3333;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background-color 0.3s;
    margin-top: 20px;
  }
  
  .logout-btn:hover {
    background-color: #7c716d;
  }
  </style>