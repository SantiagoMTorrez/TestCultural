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
  
      const crearCategoria = async () => {
        try {
          const token = localStorage.getItem('token');
          const response = await fetch('http://localhost:8080/trivia/categories/create/', {
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
        crearCategoria
      };
    }
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 20px;
    background-color: #f5f5f5;
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
  </style>
  