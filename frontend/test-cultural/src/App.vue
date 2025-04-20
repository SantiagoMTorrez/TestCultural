<template>
  <div>
    <router-view @login-exitoso="handleLogin" />
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    handleLogin(token) {
      console.log("Token recibido:", token);
      localStorage.setItem("auth_token", token); // guarda el token localmente
      this.$router.push('/bienvenida'); // redirige a otra página tras login
    }
  }
};
</script>
