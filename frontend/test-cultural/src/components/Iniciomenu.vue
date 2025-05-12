<template>
  <div class="menu-container">
      <div class="menu-box">
    <h1>MENÚ PRINCIPAL</h1>
    <p>Aquí irá el contenido principal del test cultural.</p>
    <button @click="logout">CERRAR SESIÓN</button>
      </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
  name: 'InicioMenu',
  setup() {
    const router = useRouter();

    onMounted(() => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Debes iniciar sesión primero.');
        router.push('/');
      }
    });

    const logout = () => {
      localStorage.removeItem('token');
      router.push('/');
    };

    return { logout };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

.menu-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: url('@/assets/patrones.png') repeat-y top center;
  background-size: contain;
  background-color: #f5f5f5;
  text-align: center;
  font-family: 'Jeju Hallasan', cursive;
}

.menu-box {
background: rgba(255, 255, 255, 0.95);
padding: 2.5rem 2rem;
border-radius: 20px;
box-shadow: 0 0 15px #00000055;
text-align: center;
max-width: 600px;
width: 100%;
}
h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #800000;
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #333;
}

button {
  background: #c0392b;
  border: none;
  color: white;
  padding: 12px 25px;
  border-radius: 10px;
  font-size: 1.2rem;
  font-family: 'Jeju Hallasan', cursive;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #922b21;
}
</style>
