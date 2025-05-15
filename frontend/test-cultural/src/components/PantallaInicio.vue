<template>
  <div class="pantalla-inicio">
    <div class="contenido">
      <div class="texto">
        <h1>Celebrando el Bicentenario de Bolivia</h1>
        <p>
          El Bicentenario de Bolivia representa 200 años de lucha, identidad y cultura. Es un momento para reflexionar sobre nuestra historia, celebrar nuestros logros y mirar hacia un futuro más justo y unido. ¡Únete a esta conmemoración histórica!
        </p>
      </div>

      <div class="carrusel">
        <img :src="imagenes[indice]" alt="Imagen Bicentenario" />
      </div>
    </div>

    <div class="carrusel-departamentos-contenedor">
      <button class="flecha izquierda" @click="moverIzquierda"></button>

      <div
        class="carrusel-departamentos-wrapper"
        ref="carrusel"
        @mouseenter="pausarAnimacion"
        @mouseleave="reanudarAnimacion"
      >
        <div class="carrusel-departamentos">
          <div
            class="departamento"
            v-for="(dep, i) in departamentos"
            :key="i"
            @click="seleccionarDepartamento(dep)"
          >
            <div class="departamento-card">
              {{ dep.nombre }}
            </div>
          </div>
        </div>
      </div>

      <button class="flecha derecha" @click="moverDerecha"></button>
    </div>

    <div v-if="departamentoSeleccionado" class="descripcion-departamento">
      <h3>{{ departamentoSeleccionado.nombre }}</h3>
      <p>{{ departamentoSeleccionado.descripcion }}</p>
    </div>

    <div class="diversidad-info">
      <div class="texto-diversidad">
        <h2>La diversidad boliviana</h2>
        <p>
          Bolivia es un país plurinacional con una rica diversidad cultural, geográfica y lingüística. Desde los Andes hasta el Chaco, y la Amazonía hasta los valles, cada rincón refleja una identidad única. Con más de 30 pueblos originarios, Bolivia celebra su pluralidad como una de sus mayores riquezas.
        </p>
      </div>
    </div>

    <div class="texto-final">
      <h2>¿Cuánto conoces de Bolivia?</h2>
      <p>Pon a prueba tu conocimiento con nuestro test cultural.</p>
      <button @click="irAlLogin">INICIAR</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PantallaInicio',
  data() {
    return {
      imagenes: [
        require('@/assets/bo1.jpg'),
        require('@/assets/bo2.jpg'),
        require('@/assets/bo3.jpg')
      ],
      indice: 0,
      scrollTimer: null,
      estaPausado: false,
      departamentoSeleccionado: null,
      departamentos: [
        { nombre: 'La Paz', descripcion: 'La Paz es la sede de gobierno y alberga el Illimani, el lago Titicaca y la ciudad más alta del mundo. Su riqueza cultural aymara y sus paisajes la hacen única.' },
        { nombre: 'Cochabamba', descripcion: 'Cochabamba es conocida como el “granero de Bolivia” por su fertilidad. Tiene un clima primaveral y es famosa por su gastronomía y espíritu alegre.' },
        { nombre: 'Santa Cruz', descripcion: 'Santa Cruz es el motor económico del país. Su capital es moderna, multicultural y está rodeada de una biodiversidad amazónica excepcional.' },
        { nombre: 'Oruro', descripcion: 'Oruro es famosa por su Carnaval, Patrimonio de la Humanidad. Tiene una rica historia minera y una fuerte tradición andina.' },
        { nombre: 'Potosí', descripcion: 'Potosí fue una de las ciudades más ricas del mundo por su Cerro Rico. Hoy destaca por su legado colonial y por el impresionante Salar de Uyuni.' },
        { nombre: 'Chuquisaca', descripcion: 'Chuquisaca alberga Sucre, capital constitucional de Bolivia y cuna de la independencia. Conserva su arquitectura colonial y cultura jurídica.' },
        { nombre: 'Tarija', descripcion: 'Tarija es tierra de valles cálidos, viñedos y música tradicional. Destaca por la producción de singani y su ambiente tranquilo.' },
        { nombre: 'Beni', descripcion: 'Beni es un departamento amazónico con extensas pampas, ríos navegables y cultura indígena viva. Su economía gira en torno a la ganadería.' },
        { nombre: 'Pando', descripcion: 'Pando es la región más selvática del país. Rica en castaña y biodiversidad, comparte una intensa vida fronteriza con Brasil.' }
      ]
    };
  },
  mounted() {
    this.iniciarCarrusel();
    this.autoScroll();
  },
  beforeUnmount() {
    clearInterval(this.scrollTimer);
    clearInterval(this.intervalo);
  },
  methods: {
    iniciarCarrusel() {
      this.intervalo = setInterval(() => {
        this.indice = (this.indice + 1) % this.imagenes.length;
      }, 3000);
    },
    autoScroll() {
      this.scrollTimer = setInterval(() => {
        if (!this.estaPausado && this.$refs.carrusel) {
          this.$refs.carrusel.scrollLeft += 1;
        }
      }, 20);
    },
    pausarAnimacion() {
      this.estaPausado = true;
    },
    reanudarAnimacion() {
      this.estaPausado = false;
    },
    moverIzquierda() {
      this.$refs.carrusel.scrollLeft -= 300;
    },
    moverDerecha() {
      this.$refs.carrusel.scrollLeft += 300;
    },
    seleccionarDepartamento(dep) {
      this.departamentoSeleccionado = dep;
    },
    irAlLogin() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');

.pantalla-inicio {
  font-family: 'Jeju Hallasan', cursive;
  background: url('@/assets/patron-move.gif') repeat-y top center;
  background-size: 100% auto;
  background-color: #F7B787;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.contenido {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  max-width: 1100px;
}

.texto {
  background: #F9E8D9;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.texto h1 {
  color: #527853;
  font-size: 2rem;
}

.texto p {
  font-size: 1.2rem;
  color: #333;
}

.carrusel img {
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
}

.carrusel-departamentos-contenedor {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
  width: 100%;
  max-width: 1100px;
}

.flecha {
  background-color: #527853;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  position: relative;
}

.flecha::before {
  content: '';
  border: solid white;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 7px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.flecha.izquierda::before {
  transform: translate(-50%, -50%) rotate(135deg);
}

.flecha.derecha::before {
  transform: translate(-50%, -50%) rotate(-45deg);
}

.carrusel-departamentos-wrapper {
  flex: 1;
  overflow: hidden;
  cursor: grab;
}

.carrusel-departamentos {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  white-space: nowrap;
}

.departamento-card {
  background-color: #F9E8D9;
  padding: 2rem;
  border-radius: 12px;
  min-width: 200px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: #527853;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s, background-color 0.2s;
}

.departamento-card:hover {
  background-color: #edd3b4;
  transform: scale(1.05);
  cursor: pointer;
}

.descripcion-departamento {
  background-color: #fff3e6;
  border-left: 6px solid #527853;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  border-radius: 8px;
  max-width: 900px;
}

.descripcion-departamento h3 {
  color: #527853;
  font-size: 1.5rem;
}

.descripcion-departamento p {
  font-size: 1.1rem;
  color: #333;
}

.diversidad-info {
  background-color: #F9E8D9;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  max-width: 900px;
}

.texto-diversidad h2 {
  font-size: 1.5rem;
  color: #527853;
}

.texto-diversidad p {
  font-size: 1.1rem;
  color: #333;
}

.texto-final {
  text-align: center;
  background-color: #F9E8D9;
  padding: 1rem;
  border-radius: 10px;
  max-width: 600px;
}

.texto-final h2 {
  font-size: 1.8rem;
  color: #527853;
}

.texto-final p {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.texto-final button {
  background-color: #527853;
  color: white;
  padding: 0.8rem 1.6rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.texto-final button:hover {
  background-color: #3e6044;
}
</style>
