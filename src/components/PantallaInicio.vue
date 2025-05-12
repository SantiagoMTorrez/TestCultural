<template>
    <div class="pantalla-inicio">
      <div class="contenido">
        <div class="texto">
          <h1>Celebrando el Bicentenario de Bolivia</h1>
          <p>
            El Bicentenario de Bolivia representa 200 años de lucha, identidad y cultura. Es un momento para reflexionar sobre nuestra historia, celebrar nuestros logros y mirar hacia un futuro más justo y unido. ¡Únete a esta conmemoración histórica!
          </p>
        </div>
  
        <div class="carrusel">
          <img :src="imagenes[indice]" alt="Imagen Bicentenario" />
        </div>
      </div>
  
      <div class="texto-final">
        <h2>¿Cuánto conoces de Bolivia?</h2>
        <p>Pon a prueba tu conocimiento con nuestro test cultural.</p>
        <button @click="irAlLogin">INICIAR</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PantallaInicio',
    data() {
      return {
        imagenes: [
          require('@/assets/bo1.jpg'),
          require('@/assets/bo2.jpg'),
          require('@/assets/bo3.jpg')
        ],
        indice: 0,
      };
    },
    mounted() {
      setInterval(() => {
        this.indice = (this.indice + 1) % this.imagenes.length;
      }, 3000); // cambia cada 3 segundos
    },
    methods: {
      irAlLogin() {
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
  
  .pantalla-inicio {
    font-family: 'Jeju Hallasan', cursive;
    min-height: 100vh;
    width: 100vw;
    background: url('@/assets/patron-move.gif') repeat-y top center;
    background-size: 100% auto;
    background-color: #F7B787;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
  }
  
  .contenido {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
    max-width: 1100px;
  }
  
  .texto {
    flex: 1;
    background: #F9E8D9;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  .texto h1 {
    color: #527853;
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .texto p {
    font-size: 1.2rem;
    color: #333;
  }
  
  .carrusel {
    flex: 1;
    max-width: 500px;
    height: auto;
  }
  
  .carrusel img {
    width: 100%;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    transition: opacity 0.5s ease-in-out;
  }
  
  .texto-final {
    text-align: center;
    margin-top: 2rem;
    background-color: #F9E8D9;
    padding: 1rem;
    border-radius: 10px;
    width: 100%;
    max-width: 600px;
  }
  
  .texto-final h2 {
    font-size: 1.8rem;
    color: #527853;
  }
  
  .texto-final p {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  
  .texto-final button {
    background-color: #527853;
    color: white;
    padding: 0.8rem 1.6rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .texto-final button:hover {
    background-color: #3e6044;
  }
  </style>
  