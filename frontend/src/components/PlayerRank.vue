<template>
  <div class = "roller">
    <div class="ranking-container">
      <h2 class="ranking-title">Ranking de Jugadores</h2>
  
      <div v-if="loading" class="loading">Cargando ranking...</div>
  
      <div v-else>
        <table class="ranking-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre</th>
              <th>Email</th>
              <th>Puntos</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(player, index) in ranking"
              :key="player.email"
              :class="{ 'top-player': index < 3 }"
            >
              <td>
                <span v-if="index === 0">🥇</span>
                <span v-else-if="index === 1">🥈</span>
                <span v-else-if="index === 2">🥉</span>
                <span v-else>{{ index + 1 }}</span>
              </td>
              <td>{{ player.name }}</td>
              <td>{{ player.email }}</td>
              <td>{{ player.points.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <button class="back-btn" @click="goBack">← Volver</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'RankingView',
  setup() {
    const ranking = ref([]);
    const loading = ref(true);
    const router = useRouter();

    onMounted(async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }
      try {
        const response = await fetch(
          `http://${window.location.hostname}:8080/trivia/test/player-rank/`,
          {
            headers: {
              accept: 'application/json',
              Authorization: `Token ${token}`,
            },
          }
        );
        if (response.ok) {
          ranking.value = await response.json();
        } else {
          console.error('Error al obtener el ranking:', response.statusText);
        }
      } catch (error) {
        console.error('Error de red al obtener el ranking:', error);
      } finally {
        loading.value = false;
      }
    });

    const goBack = () => {
      router.go(-1);
    };

    return {
      ranking,
      loading,
      goBack,
    };
  },
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

body {
  background: var(--c-bg);
}
</style>

<style scoped>

.roller{
  background-size: cover;
  background-repeat: no-repeat;
  background-image: url('@/assets/patron-move.gif');
}

.ranking-container {
  max-width: 800px;
  padding: 1.5rem;
  height: 100vh;
  width: fit-content;
  margin: auto;
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);

}

.ranking-title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: var(--c-primary);
  text-align: center;
}

.loading {
  text-align: center;
  font-size: 1.1rem;
  color: var(--c-text);
  padding: 1rem 0;
}

.ranking-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  overflow: hidden;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.ranking-table th,
.ranking-table td {
  padding: 0.75rem 1rem;
  text-align: center;
  font-size: 1rem;
  border-bottom: 1px solid #ddd;
}

.ranking-table th {
  background: var(--c-primary);
  color: #fff;
  font-weight: bold;
}

.ranking-table tr:nth-child(even) td {
  background: #f9f9f9;
}

.top-player td {
  background: #ffeaa7;
  font-weight: bold;
}

.back-btn {
  display: block;
  margin: 1.5rem auto 0;
  padding: 0.75rem 2rem;
  background: var(--c-secondary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.back-btn:hover {
  background: var(--c-primary);
}

#app{
  background: black;
}
</style>
