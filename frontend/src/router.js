import { createRouter, createWebHistory } from 'vue-router';
import FormularioLogin from '@/components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import BienvenidaForm from '@/components/BienvenidaForm.vue';
import MainForm from '@/components/MainForm.vue';
import QuizStart from '@/components/QuizStart.vue';
import StaffMain from '@/components/StaffMain.vue';
import NuevaPreguntas from '@/components/nuevaPreguntas.vue';
import NuevaCategoria from '@/components/nuevaCategoria.vue';
import CategoriasTabla from './components/CategoriasTabla.vue';
import PreguntasTabla from './components/PreguntasTabla.vue';
import RevisarRespuestas from './components/RevisarRespuestas.vue';
import QuizGeneric from './components/QuizGeneric.vue';
import PantallaInicio from './components/PantallaInicio.vue';
import GreatingNotification from './components/GreatingNotification.vue';
import FailedNotification from './components/FailedNotification.vue';
import Results from './components/Resultados.vue';
import ModoEducativo from './components/ModoEducativo.vue';

const routes = [
  {
    path: "/login",
    name: "Login",
    component: FormularioLogin,
  },
  {
    path: "/modoEducativo",
    name: "ModoEducativo",
    component: ModoEducativo,
  },
  {
    path: "/bienvenida",
    name: "Bienvenida",
    component: BienvenidaForm,
  },
  {
    path: "/",
    name: "PantallaInicio",
    component: PantallaInicio,
  },
  {
    path: "/mainform",
    name: "MainForm",
    component: MainForm,
  },
  {
    path: "/registerform",
    name: "Register",
    component: RegisterForm,
  },
  {
    path: "/quizstart",
    name: "QuizStart",
    component: QuizStart,
    props: (route) => ({
      categoryId: route.query.categoryId,
      categoryName: route.query.categoryName,
      difficulty: route.query.difficulty,
    }),
  },
  {
    path: "/staffmain",
    name: "StaffMain",
    component: StaffMain,
  },
  {
    path: "/nuevaPreguntas",
    name: "NuevaPreguntas",
    component: NuevaPreguntas,
  },
  {
    path: "/nuevaCategoria",
    name: "NuevaCategoria",
    component: NuevaCategoria,
  },
  {
    path: "/quiz",
    name: "QuizGeneric",
    component: QuizGeneric,
    props: (route) => ({
      categoryId: route.query.categoryId,
      categoryName: route.query.categoryName,
      difficulty: route.query.difficulty,
    }),
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  },
  {
    path: "/categoriasTabla",
    name: "CategoriasTabla",
    component: CategoriasTabla,
  },
  {
    path: "/preguntasTabla",
    name: "PreguntasTabla",
    component: PreguntasTabla,
  },
  {
    path: "/revisarRespuestas",
    name: "RevisarRespuestas",
    component: RevisarRespuestas,
  },
  {
    path: "/kaboom",
    name: "goodAnimation",
    component: GreatingNotification,
    props: {
      message: "¡Bien hecho! Esto es un saludo de prueba",
      type: "success",
    },
  },
  {
    path: "/kaplam",
    name: "badAnimation",
    component: FailedNotification,
    props: {
      message: "Ups… eso salió mal.",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
