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
              <button class="eliminar-btn" @click="confirmarEliminacion(category)">Eliminar</button>
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
    const isLoading = ref(false);

    // Obtener categorías al montar el componente
    onMounted(async () => {
      await cargarCategorias();
    });

    const cargarCategorias = async () => {
      try {
        const response = await fetch(`http://${window.location.hostname}:8080/trivia/categories/`, {
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
    };

    const confirmarEliminacion = (category) => {
      if (confirm(`¿Estás seguro que deseas eliminar la categoría "${category.name}" y todas sus preguntas?`)) {
        eliminarCategoriaCompleta(category.id);
      }
    };

    const obtenerPreguntasDeCategoria = async (categoryId) => {
      try {
        const response = await fetch(`http://${window.location.hostname}:8080/trivia/questions/?category=${categoryId}`, {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}` 
          },
          method: "GET",
        });

        if (response.ok) {
          return await response.json();
        } else {
          console.error("Error al obtener preguntas de la categoría");
          return [];
        }
      } catch (error) {
        console.error("Error de conexión:", error);
        return [];
      }
    };

    const eliminarPregunta = async (id) => {
      try {
        const response = await fetch(`http://${window.location.hostname}:8080/trivia/questions/${id}/delete/`, {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          method: "DELETE",
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error al eliminar pregunta:", errorData);
          return false;
        }
        return true;
      } catch (error) {
        console.error("Error:", error);
        return false;
      }
    };

    const eliminarCategoria = async (id) => {
      try {
        const response = await fetch(`http://${window.location.hostname}:8080/trivia/categories/${id}/`, {
          headers: { 
            "accept": "application/json", 
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          method: "DELETE",
        });

        if (response.ok) {
          return true;
        } else {
          const errorData = await response.json();
          console.error("Error al eliminar categoría:", errorData);
          return false;
        }
      } catch (error) {
        console.error("Error:", error);
        return false;
      }
    };

    const eliminarCategoriaCompleta = async (categoryId) => {
      isLoading.value = true;
      
      try {
        // 1. Obtener todas las preguntas de esta categoría
        const preguntas = await obtenerPreguntasDeCategoria(categoryId);
        
        // 2. Eliminar todas las preguntas
        if (preguntas.length > 0) {
          const resultados = await Promise.all(
            preguntas.map(pregunta => eliminarPregunta(pregunta.id))
          );
          
          const errores = resultados.filter(exito => !exito);
          if (errores.length > 0) {
            alert(`No se pudieron eliminar ${errores.length} preguntas. La categoría no se eliminará.`);
            return;
          }
        }
        
        // 3. Eliminar la categoría
        const categoriaEliminada = await eliminarCategoria(categoryId);
        
        if (categoriaEliminada) {
          alert('Categoría y todas sus preguntas eliminadas correctamente');
          await cargarCategorias(); // Recargar la lista
        } else {
          alert('Error al eliminar la categoría');
        }
      } catch (error) {
        console.error("Error en el proceso de eliminación:", error);
        alert('Ocurrió un error durante el proceso de eliminación');
      } finally {
        isLoading.value = false;
      }
    };

    const salir = () => {
      router.push('/staffMain');
    };
    
    return {
      categories,
      isLoading,
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

.eliminar-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
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