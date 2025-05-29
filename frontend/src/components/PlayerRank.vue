<template>
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
            <tr v-for="(player, index) in ranking" :key="player.email" :class="{ 'top-player': index < 3 }">
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
          const response = await fetch('http://localhost:8080/trivia/test/player-rank/', {
            headers: {
              accept: 'application/json',
              Authorization: `Token ${token}`,
            },
          });
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
  
  <style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

    * {
    font-family: 'Jeju Hallasan', cursive;
    box-sizing: border-box;
    }

    .ranking-container {
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

  
  .ranking-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: #333;
    font-weight: 600;

    background-color: color-mix(in srgb, white 50%, transparent 50%);
    padding: 1em;
    border-radius: 0.5em;

  }
  
  .ranking-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2rem;
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .ranking-table th,
  .ranking-table td {
    padding: 1rem;
    text-align: center;
    font-size: 1.1rem;
    border-bottom: 1px solid #ddd;
  }
  
  .ranking-table th {
    background-color: #338bff;
    color: white;
    font-weight: bold;
  }
  
  .ranking-table tr:last-child td {
    border-bottom: none;
  }
  
  .ranking-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .ranking-table tr.top-player {
    font-weight: bold;
    background-color: #ffeaa7 !important;
    color: #2d3436;
  }
  
  .loading {
    font-size: 1.2rem;
    color: #555;
    margin: 2rem 0;
  }
  
  .back-btn {
    padding: 12px 25px;
    background-color: #6D004D;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .back-btn:hover {
    background-color: #52003B;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>