import { createRouter, createWebHistory } from 'vue-router';
import FormularioLogin from '@/components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import BienvenidaForm from '@/components/BienvenidaForm.vue';
import MainForm from '@/components/MainForm.vue'; // Importa el nuevo MainForm
import QuizStart from '@/components/QuizStart.vue';
import StaffMain from '@/components/StaffMain.vue';
import NuevaPreguntas from '@/components/nuevaPreguntas.vue'; 
import NuevaCategoria from '@/components/nuevaCategoria.vue';
import CategoriasTabla from './components/CategoriasTabla.vue';  
import PreguntasTabla from './components/PreguntasTabla.vue';
import Resultados from './components/Resultados.vue';
import RevisarRespuestas from './components/RevisarRespuestas.vue';
import QuizGeneric from './components/QuizGeneric.vue';
import PantallaInicio from './components/PantallaInicio.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: FormularioLogin
  },
  {
    path: '/bienvenida',
    name: 'Bienvenida',
    component: BienvenidaForm
  },
  {
    path: '/',
    name: 'PantallaInicio',
    component: PantallaInicio
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
  },
  {
    path: '/quizGeneric',
    name: 'QuizGeneric',
    component: QuizGeneric,
  },
  {
    path: '/resultados',
    name: 'Resultados',
    component: Resultados,
  },
  {
    path: '/categoriasTabla',
    name: 'CategoriasTabla',  
    component: CategoriasTabla,
  },
  {
    path: '/preguntasTabla',
    name: 'PreguntasTabla', 
    component: PreguntasTabla,
  },
  {
    path: '/revisarRespuestas',
    name: 'RevisarRespuestas',
    component: RevisarRespuestas,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
