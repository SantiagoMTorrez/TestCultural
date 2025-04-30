<template>
  <div class="container">
    <div class="card">
      <h2>Ingrese<br />BICENTENARIO DE BOLIVIA</h2>
      
      <form @submit.prevent="registrar">
        <div class="form-group">
          <label for="pregunta">Ingrese una pregunta:</label>
          <input type="text" id="pregunta" v-model="pregunta" required />
        </div>
        
        <div class="form-group">
          <label for="explicacion">Ingrese la explicación:</label>
          <input type="text" id="explicacion" v-model="explicacion" required />
        </div>

        <div class="form-group">
          <label for="score">Ingrese el valor:</label>
          <input type="number" id="score" v-model="score" required />
        </div>
        
        <div class="form-group">
          <label for="categoria">Elija una categoría:</label>
          <select id="categoria" v-model="selectedCategory" required>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="dificultad">Elija la dificultad:</label>
          <select id="dificultad" v-model="dificultad" required>
            <option value="Fácil">Fácil</option>
            <option value="Medio">Medio</option>
            <option value="Difícil">Difícil</option>
            <option value="Intenso">Intenso</option>
          </select>
        </div>

        <div class="form-group">
          <label for="respuestaCorrecta">Ingrese la respuesta correcta:</label>
          <input type="text" id="respuestaCorrecta" v-model="respuestaCorrecta" required />
        </div>

        <div class="form-group">
          <label for="respuesta1">Ingrese una respuesta incorrecta:</label>
          <input type="text" id="respuesta1" v-model="respuesta1" required />
        </div>

        <div class="form-group">
          <label for="respuesta2">Ingrese una respuesta incorrecta:</label>
          <input type="text" id="respuesta2" v-model="respuesta2" required />
        </div>

        <div class="form-group">
          <label for="respuesta3">Ingrese una respuesta incorrecta:</label>
          <input type="text" id="respuesta3" v-model="respuesta3" required />
        </div>

        <button type="submit" class="submit-btn">Registrar</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: "NuevaPreguntas",
  setup() {
    const router = useRouter();
    
    // Datos del formulario
    const pregunta = ref('');
    const explicacion = ref('');
    const score = ref('');
    const selectedCategory = ref('');
    const dificultad = ref('Fácil');
    const respuestaCorrecta = ref('');
    const respuesta1 = ref('');
    const respuesta2 = ref('');
    const respuesta3 = ref('');
    const categories = ref([]);

    // Obtener categorías al montar el componente
    onMounted(async () => {
      try {
        const response = await fetch("http://localhost:8080/trivia/categories/", {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}` 
          },
          method: "GET",
        });

        if (response.ok) {
          categories.value = await response.json();
        } else {
          console.error("Error al obtener categorías");
        }
      } catch (error) {
        console.error("Error de conexión:", error);
      }
    });

    const registrar = async () => {
      try {
        // Convertir dificultad a FK
        let dificultadFK = 0;
        switch (dificultad.value) {
          case "Fácil":
            dificultadFK = 1;
            break;
          case "Medio":
            dificultadFK = 2;
            break;
          case "Difícil":
            dificultadFK = 3;
            break;
          case "Intenso":   
            dificultadFK = 4;
            break;
          default:
            break;
        }

       

        const tokenValor = localStorage.getItem('token');

        console.log("Enviando pregunta:");

        const response = await fetch("http://localhost:8080/trivia/questions/create/", {
          headers: { 
            "Content-Type": "application/json", "Authorization" : "Token " + tokenValor},
          method: "POST",
          body: JSON.stringify(
            {
              text:pregunta.value,
              explanation:explicacion.value,
              difficulty: dificultadFK,
              score: score.value,
              category: selectedCategory.value,
              question_type: 1,
              answer_options: [
                { text: respuestaCorrecta.value, correct: true },
                { text: respuesta1.value, correct: false },
                { text: respuesta2.value, correct: false },
                { text: respuesta3.value, correct: false }
              ]
            }
          )
        });

        if (response.ok) {
          alert("Pregunta registrada con éxito.");
          router.push('/staffMain');
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Error al registrar la pregunta.");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("No se pudo conectar al servidor.");
      }
    };
    
    return {
      pregunta,
      explicacion,
      score,
      selectedCategory,
      dificultad,
      respuestaCorrecta,
      respuesta1,
      respuesta2,
      respuesta3,
      categories,
      registrar
    };
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 600px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #34495e;
}

input, select {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input:focus, select:focus {
  outline: none;
  border-color: #3498db;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #27ae60;
}

@media (max-width: 768px) {
  .card {
    padding: 20px;
  }
}
</style>