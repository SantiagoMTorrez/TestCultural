import { createRouter, createWebHistory } from 'vue-router';
import FormularioLogin from '@/components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import BienvenidaForm from '@/components/BienvenidaForm.vue';
import MainForm from '@/components/MainForm.vue'; // Importa el nuevo MainForm
import QuizStart from '@/components/QuizStart.vue';
import StaffMain from '@/components/StaffMain.vue';
import NuevaPreguntas from '@/components/nuevaPreguntas.vue'; 
import NuevaCategoria from '@/components/nuevaCategoria.vue'; 

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
    path: '/mainform', // Cambia la ruta a /mainform
    name: 'MainForm',  // Ruta para el formulario principal
    component: MainForm
  },
  {
    path: '/registerform',
    name: 'Register',
    component: RegisterForm
  },
  {
    path: '/quiz',
    name: 'QuizStart',
    component: QuizStart
  },
  {
    path: '/staffmain',
    name: 'StaffMain',
    component: StaffMain
  },
  {
    path: '/nuevaPreguntas',
    name: 'NuevaPreguntas',
    component: NuevaPreguntas
  },
  {
    path: '/nuevaCategoria',
    name: 'NuevaCategoria',
    component: NuevaCategoria
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;