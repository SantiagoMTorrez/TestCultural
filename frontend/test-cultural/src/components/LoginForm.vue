<template>
  <div class="container">
    <div class="card">
      <h2>TEST CULTURAL DEL<br />BICENTENARIO DE BOLIVIA</h2>

      <label for="email"><em>E-mail:</em></label>
      <input v-model="email" type="email" id="email" required />

      <label for="password"><em>Contraseña:</em></label>
      <input v-model="password" type="password" id="password" required />

      <div class="buttons">
        <button @click="login">INICIAR SESIÓN</button>
        <button @click="irARegistro">REGISTRARSE</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  name: "LoginForm",
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const token = ref('');

    const login = async () => {
      try {
        const loginData = {
          email: email.value,
          password: password.value
        };

        console.log("Enviando login:", loginData); // Verifica qué estás enviando

        const response = await fetch("http://localhost:8080/user/login/", {
          headers: { "Content-Type": "application/json" },
          method: "POST",
          body: JSON.stringify(loginData)
        });

        if (response.ok) {
          const data = await response.json();
          token.value = data.token;
          localStorage.setItem('token', token.value);
          localStorage.setItem('dataname', data.name); // guarda el nombre del usuario
          router.push('/bienvenida');
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Correo o contraseña incorrectos.");
        }
      } catch (error) {
        alert("No se pudo conectar al servidor.");
      }
    };

    const irARegistro = () => {
      router.push('/registerform');
    };

    return { email, password, login, irARegistro };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('@/assets/patrones.png') repeat-y top center;
  background-size: contain;
  background-color: #f5f5f5;
}

.card {
  font-family: 'Jeju Hallasan', cursive;
  background: #b7ded3;
  padding: 30px;
  border-radius: 15px;
  width: 400px;
  text-align: center;
  border: 5px solid #800000;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

input {
  display: block;
  width: 90%;
  margin: 10px auto;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #888;
  font-size: 1rem;
}

label {
  display: block;
  margin-top: 15px;
  font-size: 1.2rem;
}

.buttons {
  margin-top: 20px;
}

button {
  background: orange;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-family: 'Jeju Hallasan', cursive;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: darkorange;
}
</style>
