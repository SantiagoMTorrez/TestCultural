<template>
  <div class="bienvenida-container">
    <div class="bienvenida-box">
      <div class="perfil">
        <img src="@/assets/avatar.png" alt="Avatar" class="avatar" />
        <p class="nombre">{{ dataname }}</p>
      </div>
      <h1>¡BIENVENIDO!</h1>
      <h2>TEST CULTURAL DEL BICENTENARIO DE BOLIVIA</h2>
      <button @click="irAlMenu">EMPEZAR</button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';

export default {
  dataname: 'BienvenidaForm',
  setup() {
    const router = useRouter();
    const dataname = ref('');

    onMounted(() => {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Debes iniciar sesión primero.');
        router.push('/');
        return;
      }

      const nombre = localStorage.getItem('dataname');
      dataname.value = nombre ? nombre : 'Usuario';
    });

    const irAlMenu = () => {
      router.push('/iniciomenu');
    };

    return { irAlMenu, dataname };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
}

.bienvenida-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/assets/patrones.png');
  background-size: cover;
}

.bienvenida-box {
  background: rgba(255, 255, 255, 0.95);
  padding: 2.5rem 2rem;
  border-radius: 20px;
  box-shadow: 0 0 15px #00000055;
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.perfil {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 1.5rem;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ddd;
}

.nombre {
  font-size: 1.2rem;
  font-weight: bold;
}

h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

h2 {
  font-size: 1.3rem;
  color: #6d004d;
  margin-bottom: 30px;
}

button {
  background-color: #b33030;
  color: white;
  padding: 0.9rem 2rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #8c2222;
}
</style>
