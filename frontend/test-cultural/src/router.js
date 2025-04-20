// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import FormularioLogin from '@/components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import BienvenidaForm from '@/components/BienvenidaForm.vue';
import Iniciomenu from '@/components/Iniciomenu.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: FormularioLogin
  },
  {
    path: '/bienvenida',
    name: 'Bienvenida',
    component: BienvenidaForm
  },
  {
    path: '/iniciomenu',
    name: 'InicioMenu',
    component: Iniciomenu
  },
  {
    path: '/registerform',
    name: 'Register',
    component: RegisterForm
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
