<template>
  <div class="container">
    <div class="card">
      <h2><br>LISTA DE PREGUNTAS<br></h2>
      
      <table class="questions-table">
        <thead>
          <tr>
            <th>Pregunta</th>
            <th>Dificultad</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id">
            <td>{{ question.text }}</td>
            <td>{{ getDificultadText(question.difficulty) }}</td>
            <td>
              <button class="eliminar-btn" @click="confirmarEliminacion(question.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>

      <button class="salir-btn" @click="salir">Salir</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "PreguntasTabla",
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

    const confirmarEliminacion = (id) => {
      if (confirm('¿Estás seguro que deseas eliminar esta pregunta?')) {
        eliminarPregunta(id);
      }
    };

    const eliminarPregunta = async (id) => {
      try {
        const response = await fetch(`http://localhost:8080/trivia/questions/${id}/delete/`, {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          method: "DELETE",
        });

        if (response.ok) {
          alert('Pregunta eliminada correctamente');
          await cargarPreguntas(); // Recargar la lista después de eliminar
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Error al eliminar la pregunta");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("No se pudo conectar al servidor");
      }
    };

    const salir = () => {
      console.log('Saliendo...');
      router.push('/staffMain');
    };
    
    return {
      questions,
      getDificultadText,
      confirmarEliminacion,
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
  padding: 50px;
}

.card {
  background: rgb(255, 255, 255);
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 50px;
  width: 100%;
  max-width: 800px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 24px;
}

.questions-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}

.questions-table th, .questions-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.questions-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #34495e;
}

.questions-table tr:hover {
  background-color: #f5f5f5;
}

.eliminar-btn {
  padding: 8px 15px;
  background-color: #ff3333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.eliminar-btn:hover {
  background-color: #cc0000;
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
  
  .questions-table {
    display: block;
    overflow-x: auto;
  }
}
</style>