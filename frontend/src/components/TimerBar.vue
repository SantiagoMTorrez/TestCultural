<template>
  <div class="timer-bar">
    <canvas ref="progressBar"></canvas>
  </div>
</template>

<script>
export default {
  name: 'TimerBarCanvas',
  props: {
    duration: {           
      type: Number,
      default: 0
    },
    reverse: {             
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      began: 0,            
      animationFrameId: 0, 
      ctx: null,          
      canvasW: 0,          
      canvasH: 0           
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
      this.ctx.clearRect(0, 0, this.canvasW, this.canvasH);
      this.ctx.fillRect(0, 0, this.canvasW * progress, this.canvasH);

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
