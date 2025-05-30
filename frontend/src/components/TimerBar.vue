<template>
  <div class="timer-bar">
    <canvas ref="progressBar"></canvas>
  </div>
</template>

<script>
export default {
  name: 'TimerBarCanvas',
  props: {
    duration: {            // Duración en segundos
      type: Number,
      default: 0
    },
    reverse: {             // Indicador de sentido inverso
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      began: 0,            // Tiempo de inicio en ms
      animationFrameId: 0, // ID de RAF
      ctx: null,           // Contexto 2D
      canvasW: 0,          // Anchura cacheada
      canvasH: 0           // Altura cacheada
    };
  },
  watch: {
    duration() {
      this.restartAnimation();
    }
  },
  mounted() {
    const canvas = this.$refs.progressBar;
    // Ajuste de resolución al tamaño real del contenedor
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Cachear contexto, estilo y dimensiones
    this.ctx      = canvas.getContext('2d');
    this.ctx.fillStyle = '#2ecc71';
    this.canvasW = canvas.width;
    this.canvasH = canvas.height;

    this.restartAnimation();
  },
  methods: {
    restartAnimation() {
      this.began = performance.now();
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = requestAnimationFrame(this.update);
    },
    update() {
      const now = performance.now();
      let progress = (now - this.began) / (this.duration * 1000);
      if (progress >= 1) return;
      if (this.reverse) progress = 1 - progress;
      // Dibujar un único clear + fill
      this.ctx.clearRect(0, 0, this.canvasW, this.canvasH);
      this.ctx.fillRect(0, 0, this.canvasW * progress, this.canvasH);

      // Programar siguiente fotograma
      this.animationFrameId = requestAnimationFrame(this.update);
    }
  }
};
</script>

<style scoped>
.timer-bar {
  width: 100%;
  height: 10px;
  background-color: #ddd;
  border-radius: 5px;
  overflow: hidden;
}
.timer-bar canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
