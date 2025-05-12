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
}
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 93vh;
    padding: 20px;
    background-image: url('@/assets/patrones.png');
  }
  
  .card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    max-width: 500px;
    width: 100%;
  }
  
  h2 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    font-weight: 500;
    display: block;
    margin-bottom: 5px;
  }
  
  input, textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #3498db;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .submit-btn:hover {
    background-color: #2980b9;
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

  </style>
  