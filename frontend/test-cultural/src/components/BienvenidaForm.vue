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
      console.log(localStorage.getItem('staff'));
      if (localStorage.getItem('staff')=='false') {
        console.log('Redirigiendo a /mainform');  // Confirmación en consola de la redirección  
        router.push('/mainform');  // Redirigir a /mainform
      } else {
        console.log('Redirigiendo a /staff');  // Confirmación en consola de la redirección  
        router.push('/staffmain');  // Redirigir a /staff
      }
      
    };

    return { irAlMenu, dataname };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
  box-sizing: border-box;
}

.bienvenida-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-image: url('@/assets/patron-move.gif');
  background-size: cover;
  background-repeat: repeat;
  background-position: center;
}

.bienvenida-box {
  background: rgba(255, 255, 255, 0.95);
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 500px;
  width: 100%;
  animation: fadeIn 1s ease-in-out;
}

.perfil {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 1.5rem;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #ccc;
  object-fit: cover;
}

.nombre {
  font-size: 1.3rem;
  color: #333;
  font-weight: bold;
}

h1 {
  font-size: 2.2rem;
  color: #527853;
  margin-bottom: 0.8rem;
}

h2 {
  font-size: 1.4rem;
  color: #8c2222;
  margin-bottom: 2rem;
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>