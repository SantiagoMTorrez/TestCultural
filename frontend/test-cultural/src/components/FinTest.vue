<template>
  <div class="fin-container">
    <div class="result-card">
      <h2>Final del test</h2>
      <p class="result-message">Lograste responder correctamente:</p>
      <p class="result-score">{{ respuestas }} de 10</p>
      <button @click="goBack" class="back-btn">Volver al inicio</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'FinTest',
  setup() {
    const router = useRouter();
    const respuestas = ref(0);

    onMounted(() => {
      respuestas.value = parseInt(localStorage.getItem('respuestas')) || 0;
      // Limpiar almacenamiento
      localStorage.removeItem('preguntas');
      localStorage.removeItem('puntero');
      localStorage.removeItem('respuestas');
      localStorage.removeItem('idCategoria');
    });

    const goBack = () => {
      router.push('/mainform');
    };

    return {
      respuestas,
      goBack
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
}

.fin-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/patrones.png');
  padding: 20px;
}

.result-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 40px;
  max-width: 500px;
  width: 90%;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.result-message {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.result-score {
  font-size: 2rem;
  font-weight: bold;
  color: #6d004d;
  margin-bottom: 30px;
}

.back-btn {
  padding: 12px 30px;
  background-color: #6d004d;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #52003b;
}
</style>