<template>
  <div class="container">
    <div class="card">
      <h2><br>LISTA DE CATEGORÍAS<br></h2>
      
      <table class="categories-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.name }}</td>
            <td>{{ category.description }}</td>
            <td>
              <button class="eliminar-btn" @click="eliminarCategoria(category.id)">Eliminar</button>
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
  name: "CategoriasTabla",
  setup() {
    const router = useRouter();
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

    const eliminarCategoria = (id) => {
      localStorage.setItem('categoriaId', id);
      // Aquí podrías agregar lógica para eliminar la categoría si es necesario
      console.log('ID de categoría a eliminar:', id);
    };

    const salir = () => {
      console.log('Saliendo...');
      router.push('/staffMain');
    };
    
    return {
      categories,
      eliminarCategoria,
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

.categories-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}

.categories-table th, .categories-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.categories-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #34495e;
}

.categories-table tr:hover {
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
  
  .categories-table {
    display: block;
    overflow-x: auto;
  }
}
</style>