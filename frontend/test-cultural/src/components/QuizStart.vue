<template>
    <div class="quiz-container">
      <h2>Iniciando el cuestionario...</h2>
      <p>En breve verás las preguntas del cuestionario basado en la categoría y dificultad seleccionadas.</p>
      <button @click="startQuiz">Comenzar Cuestionario</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      startQuiz() {
        // Aquí iría la lógica para iniciar el cuestionario.
        console.log('Comenzando el cuestionario...');
        // Aquí puedes hacer la llamada al backend para obtener las preguntas o continuar con el flujo.
      }
    }
  };
  </script>
  
  <style scoped>
  .quiz-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 100vh;
    background-color: #f5f5f5;
  }
  
  button {
    padding: 15px 30px;
    background-color: #6d004d;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #52003b;
  }
  </style>
  