<template>
  <div class="container">
    <div class="card">
      <h2><br>MODO EDUCATIVO<br></h2>
      
      <div class="questions-grid">
        <div v-for="question in questions" :key="question.id" class="question-card">
          <div class="card-header">
            <strong>{{ question.text }}</strong>
          </div>
          <div class="card-content">
            {{ question.explanation || "Esta pregunta no tiene explicación" }}
          </div>
          <div class="card-footer">
            <span class="difficulty-badge" :class="getDifficultyClass(question.difficulty)">
              {{ getDificultadText(question.difficulty) }}
            </span>
          </div>
        </div>
      </div>

      <button class="salir-btn" @click="salir">Salir</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "ModoEducativo",
  setup() {
    const router = useRouter();
    const questions = ref([]);

    // Función para convertir el número de dificultad a texto
    const getDificultadText = (difficulty) => {
      switch(difficulty) {
        case 1: return "Fácil";
        case 2: return "Media";
        case 3: return "Difícil";
        default: return "Desconocida";
      }
    };

    // Función para obtener la clase CSS según la dificultad
    const getDifficultyClass = (difficulty) => {
      switch(difficulty) {
        case 1: return "easy";
        case 2: return "medium";
        case 3: return "hard";
        default: return "unknown";
      }
    };

    // Obtener preguntas al montar el componente
    onMounted(async () => {
      await cargarPreguntas();
    });

    const cargarPreguntas = async () => {
      try {
        const response = await fetch("http://localhost:8080/trivia/questions/", {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}` 
          },
          method: "GET",
        });

        if (response.ok) {
          questions.value = await response.json();
        } else {
          console.error("Error al obtener preguntas");
        }
      } catch (error) {
        console.error("Error de conexión:", error);
      }
    };

    const salir = () => {
      console.log('Saliendo...');
      router.push('/mainform');
    };
    
    return {
      questions,
      getDificultadText,
      getDifficultyClass,
      salir
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/patrones.png');
  padding: 20px;
}

.card {
  background: rgb(255, 255, 255);
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 1200px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 24px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.question-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: transform 0.3s ease;
}

.question-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.card-header {
  font-size: 1.1rem;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.card-content {
  flex-grow: 1;
  margin-bottom: 15px;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.difficulty-badge {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  color: white;
}

.difficulty-badge.easy {
  background-color: #4CAF50;
}

.difficulty-badge.medium {
  background-color: #FFC107;
}

.difficulty-badge.hard {
  background-color: #F44336;
}

.difficulty-badge.unknown {
  background-color: #9E9E9E;
}

.salir-btn {
  display: block;
  margin: 0 auto;
  text-align: center;
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

.salir-btn:hover {
  background-color: #7c716d;
}

@media (max-width: 768px) {
  .card {
    padding: 20px;
  }
  
  .questions-grid {
    grid-template-columns: 1fr;
  }
}
</style>    