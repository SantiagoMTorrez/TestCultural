<template>
  <div class="failed-root" v-if="visible">
    <canvas ref="canvas" class="failed-canvas"></canvas>
    <div class="failed-content">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';

// Fragmento de escombros o explosión
class Shard {
  constructor(x, y, angle, speed, length, color) {
    this.x = x;
    this.y = y;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed;
    this.length = length;
    this.color = color;
    this.life = 1.0;
    this.rotation = Math.random() * Math.PI * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 5;
  }

  update(dt) {
    // gravedad inversa para efecto explosión hacia afuera
    this.vy -= 300 * dt;
    // arrastre proporcional
    this.vx *= (1 - dt * 1.5);
    this.vy *= (1 - dt * 1.5);

    this.x += this.vx * dt;
    this.y += this.vy * dt;

    this.rotation += this.rotationSpeed * dt;
    this.life -= dt * 0.7;
  }

  draw(ctx) {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);
    ctx.globalAlpha = Math.max(0, this.life);
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(-this.length / 2, 0);
    ctx.lineTo(this.length / 2, 0);
    ctx.stroke();
    ctx.restore();
  }
}

// Shockwave efecto progreso
class Shockwave {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.radius = 0;
    this.maxRadius = Math.max(window.innerWidth, window.innerHeight) * 0.8;
    this.life = 1.0;
  }

  update(dt) {
    const speed = this.maxRadius * 2; // completa en 0.5s
    this.radius += speed * dt;
    this.life = 1 - this.radius / this.maxRadius;
  }

  draw(ctx) {
    if (this.life <= 0) return;
    ctx.save();
    ctx.strokeStyle = `rgba(231,76,60,${this.life * 0.5})`;
    ctx.lineWidth = 10 * this.life;
    ctx.beginPath();
    ctx.arc(this.x, this.y, Math.abs(this.radius), 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }
}

export default {
  name: 'FailedNotification',
  props: {
    message: { type: String, required: true },
    duration: { type: Number, default: 3000 }
  },
  setup(props) {
    const visible = ref(false);
    const canvas = ref(null);
    let ctx, w, h;
    let shards = [];
    let shockwave = null;
    let animId;
    let startTime = performance.now();

    function initCanvas() {
      const c = canvas.value;
      w = c.width = window.innerWidth;
      h = c.height = window.innerHeight;
      ctx = c.getContext('2d');
    }

    function spawnExplosion() {
      const centerX = w / 2;
      const centerY = h / 2;
      // fragmentos
      for (let i = 0; i < 150; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 400 + 200;
        const length = Math.random() * 20 + 10;
        const color = `hsl(0, 80%, ${50 + Math.random() * 10}%)`;
        shards.push(new Shard(centerX, centerY, angle, speed, length, color));
      }
      // onda de choque
      shockwave = new Shockwave(centerX, centerY);
    }

    function animate(time) {
      const dt = (time - startTime) / 1000;
      startTime = time;
      ctx.clearRect(0, 0, w, h);

      // fondo degradado intenso
      const grad = ctx.createRadialGradient(
        w / 2, h / 2, 0,
        w / 2, h / 2, Math.max(w, h) / 1.5
      );
      grad.addColorStop(0, '#e74c3c');
      grad.addColorStop(1, '#c0392b');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // onda de choque y fragmentos
      if (shockwave) {
        shockwave.update(dt);
        shockwave.draw(ctx);
      }

      shards = shards.filter(s => s.life > 0);
      shards.forEach(s => { s.update(dt); s.draw(ctx); });

      // overlay parpadeante
      const alpha = Math.abs(Math.sin(time / 100));
      ctx.fillStyle = `rgba(255,255,255,${alpha * 0.1})`;
      ctx.fillRect(0, 0, w, h);

      animId = requestAnimationFrame(animate);
    }

    async function show() {
      visible.value = true;
      await nextTick();
      initCanvas();
      spawnExplosion();
      startTime = performance.now();
      animId = requestAnimationFrame(animate);
      setTimeout(hide, props.duration);
    }

    function hide() {
      visible.value = false;
      cancelAnimationFrame(animId);
      shards = [];
      shockwave = null;
    }

    watch(() => props.message, (msg) => {
      if (msg) show();
    });

    onMounted(() => {
      window.addEventListener('resize', initCanvas);
      show();
    });

    onUnmounted(() => {
      window.removeEventListener('resize', initCanvas);
      cancelAnimationFrame(animId);
    });

    return { visible, canvas };
  }
};
</script>

<style scoped>
.failed-root {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  overflow: hidden; pointer-events: none;
  z-index: 10000;
}
.failed-canvas {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
}
.failed-content {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(-5deg);
  font-size: 2rem;
  color: #fff;
  background: rgba(192,57,43,0.8);
  padding: 1.5rem 3rem;
  border: 3px solid #e74c3c;
  box-shadow: 0 0 20px rgba(0,0,0,0.7);
  pointer-events: auto;
  animation: shake 0.5s ease-in-out infinite;
}

@keyframes shake {
  0%   { transform: translate(-50%, -50%) rotate(-5deg); }
  25%  { transform: translate(-48%, -52%) rotate(-3deg); }
  50%  { transform: translate(-50%, -50%) rotate(-5deg); }
  75%  { transform: translate(-52%, -48%) rotate(-7deg); }
  100% { transform: translate(-50%, -50%) rotate(-5deg); }
}
</style>