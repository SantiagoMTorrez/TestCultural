<template>
  <div class="container">
    <div class="card">
      <h2>TEST CULTURAL DEL<br />BICENTENARIO DE BOLIVIA</h2>
      
      <label for="email"><em>E-mail:</em></label>
      <input v-model="email" type="email" id="email" required />

      <label for="password"><em>Contraseña:</em></label>
      <input v-model="password" type="password" id="password" required />

      <div class="buttons">
        <button @click="login" class="login-btn">INICIAR SESIÓN</button>
        <button @click="irARegistro" class="register-btn">REGISTRARSE</button>
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
          localStorage.setItem('staff', data.is_staff); // guarda el email del usuario
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

:global(html), :global(body), :global(#app) {
  margin: 0;
  padding: 0;
  height: 100%;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  background: url('@/assets/patron-move.gif') repeat-y top center;
  background-size: 100% auto;
  background-color: #F7B787;
}

.card {
  font-family: 'Jeju Hallasan', cursive;
  background: #F9E8D9; /* fondo claro */
  padding: 30px;
  border-radius: 20px;
  width: 400px;
  text-align: center;
  border: 5px solid #527853; /* borde verde musgo */
  box-shadow: 0 8px 16px rgba(0,0,0,0.25);
}

h2 {
  color: #527853; /* verde musgo */
  margin-bottom: 20px;
}

input {
  display: block;
  width: 90%;
  margin: 10px auto;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

label {
  display: block;
  margin-top: 15px;
  font-size: 1.1rem;
  color: #333;
}

.buttons {
  margin-top: 25px;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

/* Botón Iniciar Sesión */
.login-btn {
  background-color: #527853;
  border: none;
  color: white;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  font-family: 'Jeju Hallasan', cursive;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #3e5d40;
}

/* Botón Registrarse */
.register-btn {
  background-color: #EE7214;
  border: none;
  color: white;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  font-family: 'Jeju Hallasan', cursive;
  transition: background-color 0.3s;
}

.register-btn:hover {
  background-color: #d45e0f;
}
</style>