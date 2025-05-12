<template>
  <div class="registro-container">
    <div class="form-box">
      <h2>Registro</h2>
      <form @submit.prevent="registrarse">
        <input type="text" v-model="nombre" placeholder="Nombre completo" required />
        <input type="email" v-model="email" placeholder="Correo electrónico" required />
        <input type="password" v-model="password" placeholder="Contraseña" required />
        <div class="button-group">
          <button type="submit" class="registrarse-btn">Registrarse</button>
          <button type="button" class="inicio-btn" @click="volverAlInicio">Volver al inicio</button>
        </div>
        <p v-if="errorMensaje" class="error">{{ errorMensaje }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      nombre: '',
      email: '',
      password: '',
      errorMensaje: ''
    };
  },
  methods: {
    async registrarse() {
      try {
        const response = await fetch("http://localhost:8080/user/create/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: this.nombre,
            email: this.email,
            password: this.password
          })
        });

        if (response.status === 201) {
          alert("¡Registro exitoso! Ahora inicia sesión.");
          this.$router.push("/");
        } else {
          let errorData = await response.text();
          this.errorMensaje = `Error al registrarse: ${errorData}`;
        }
      } catch (err) {
        console.error("Error de red:", err);
        this.errorMensaje = "No se pudo conectar con el servidor. Verifica que el backend esté activo.";
      }
    },
    volverAlInicio() {
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

* {
  font-family: 'Jeju Hallasan', cursive;
}

.registro-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: url('@/assets/patron-move.gif') repeat-y top center;
  background-size: 100% auto;
  background-color: #F7B787;
}

.form-box {
  background-color: #F9E8D9;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
  max-width: 400px;
  width: 100%;
  text-align: center;
  border: 4px solid #527853;
}

h2 {
  color: #527853;
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 0.5rem 0;
  border: 1px solid #aaa;
  border-radius: 8px;
  font-size: 1rem;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 1rem;
}

/* Botón Registrarse - Verde */
.registrarse-btn {
  background-color: #527853;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.registrarse-btn:hover {
  background-color: #3e5d40;
}

/* Botón Volver al inicio - Naranja */
.inicio-btn {
  background-color: #EE7214;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.inicio-btn:hover {
  background-color: #d45e0f;
}

.error {
  color: red;
  margin-top: 1rem;
  font-size: 0.9rem;
}
</style>
