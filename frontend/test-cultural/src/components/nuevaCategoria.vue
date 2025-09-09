<template>
    <div class="container">
      <div class="card">
        <h2>Nueva Categoría<br />BICENTENARIO DE BOLIVIA</h2>
  
        <form @submit.prevent="crearCategoria">
          <div class="form-group">
            <label for="nombre">Nombre de la categoría:</label>
            <input type="text" id="nombre" v-model="nombre" required />
          </div>
  
          <div class="form-group">
            <label for="descripcion">Descripción:</label>
            <textarea id="descripcion" v-model="descripcion" required rows="4"></textarea>
          </div>
  
          <button type="submit" class="submit-btn">Guardar Categoría</button>
          <button type="submit" class="salir-btn" @click="salir">Salir</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'NuevaCategoria',
    setup() {
      const nombre = ref('');
      const descripcion = ref('');
      const router = useRouter();
      const salir = () => {
        console.log('Saliendo...');
        router.push('/staffMain');
      };
      const crearCategoria = async () => {
        try {
          const token = localStorage.getItem('token');
          const response = await fetch('http://localhost:8080/trivia/categories/', {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Token ${token}`
            },
            body: JSON.stringify({
              name: nombre.value,
              description: descripcion.value
            })
          });
  
          if (response.ok) {
            alert('Categoría creada exitosamente');
            router.push('/staffMain'); // Redirigir a la página principal
          } else {
            const errorData = await response.json();
            alert(errorData.message || 'Error al crear la categoría.');
          }
        } catch (error) {
          console.error('Error al conectar con el servidor:', error);
          alert('No se pudo conectar al servidor.');
        }
      };
  
      return {
        nombre,
        descripcion,
        crearCategoria,
        salir
      };
    }
  };
  </script>
 
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
  
  * {
    font-family: 'Jeju Hallasan', cursive;
    box-sizing: border-box;
  }
  
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('@/assets/patron-move.gif');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    padding: 1rem;
  }
  
  .card {
    background: #fff9f0;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    max-width: 500px;
    width: 100%;
    animation: fadeInUp 0.8s ease-out;
    border: 2px solid #f4d19b;
  }
  
  h2 {
    text-align: center;
    color: #9c5f3b;
    margin-bottom: 25px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
    display: block;
    margin-bottom: 6px;
    color: #6b3e2e;
  }
  
  input,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #e0c3a3;
    border-radius: 8px;
    background-color: #fffaf4;
    color: #5a3e2b;
    font-size: 1rem;
  }
  
  input:focus,
  textarea:focus {
    outline: none;
    border-color: #f4a261;
    box-shadow: 0 0 5px #f4a26160;
  }
  
  .submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #f4a261;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .submit-btn:hover {
    background-color: #e76f51;
  }
  
  .salir-btn {
    display: block;
    margin: 15px auto 0;
    text-align: center;
    padding: 12px 25px;
    background-color: #e63946;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: background-color 0.3s;
  }
  
  .salir-btn:hover {
    background-color: #ba3a3a;
  }
  
  /* Animación */
  @keyframes fadeInUp {
    0% {
      opacity: 0;
      transform: translateY(30px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>
  