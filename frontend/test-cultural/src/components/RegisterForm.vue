<template>
  <div class="registro-container">
    <div class="form-box">
      <h2>Registro</h2>
      <form @submit.prevent="registrarse">
        <input type="text" v-model="nombre" placeholder="Nombre completo" required />
        <input type="email" v-model="email" placeholder="Correo electrónico" required />
        <input type="password" v-model="password" placeholder="Contraseña" required />
        <div class="button-group">
          <button type="submit">Registrarse</button>
          <button type="button" @click="volverAlInicio">Volver al inicio</button>
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

        // No usamos .json() directamente por si el backend no responde como JSON
        if (response.status === 201) {
          alert("¡Registro exitoso! Ahora inicia sesión.");
          this.$router.push("/"); // Login
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
  background-image: url('@/assets/patrones.png');
  background-size: cover;
}

.form-box {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 10px #00000055;
  max-width: 400px;
  width: 100%;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 0.5rem 0;
  border: 1px solid #aaa;
  border-radius: 5px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 1rem;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  margin-top: 1rem;
  font-size: 0.9rem;
}
</style>
