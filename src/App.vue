<template>
  <div>
    <AudioMenu />
    <router-view @login-exitoso="handleLogin" />
  </div>
</template>

<script>
import AudioMenu from '@/components/AudioMenu.vue';

export default {
  name: 'App',
  components: {
    AudioMenu
  },
  methods: {
    handleLogin(token) {
      console.log("Token recibido:", token);
      localStorage.setItem("auth_token", token);
      this.$router.push('/bienvenida');
    }
  }
};
</script>
