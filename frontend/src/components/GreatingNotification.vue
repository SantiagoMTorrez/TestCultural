<template>
    <div class="notification-root" v-if="visible">
      <canvas ref="canvasEl" class="notification-canvas"></canvas>
      <div class="notification-content" :class="type">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue';
  
  // Particle for confetti
  class Particle {
    constructor(x, y, vx, vy, size, color) {
      this.x = x; this.y = y;
      this.vx = vx; this.vy = vy;
      this.size = size; this.color = color;
      this.life = 1.0;
    }
    update(dt) {
      // Gravity and drag
      const g = 300;
      const drag = 1.1;
      this.vy += g * dt;
      this.vx /= drag;
      this.vy /= drag;
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      this.life -= dt * 0.5;
    }
    draw(ctx) {
      ctx.save();
      ctx.globalAlpha = this.life;
      ctx.fillStyle = this.color;
      ctx.fillRect(this.x, this.y, this.size, this.size);
      ctx.restore();
    }
  }
  
  // Light rays
  class Ray {
    constructor(angle, maxLen, speed) {
      this.angle = angle;
      this.maxLen = maxLen;
      this.speed = speed;
      this.offset = 0;
    }
    update(dt) {
      this.offset = (this.offset + this.speed * dt) % (this.maxLen * 2);
    }
    draw(ctx, w, h) {
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      ctx.strokeStyle = 'rgba(255,255,255,0.1)';
      ctx.lineWidth = 2;
      const cx = w/2, cy = h/2;
      const start = this.offset <= this.maxLen ? this.offset : (2*this.maxLen - this.offset);
      const x1 = cx + Math.cos(this.angle) * start;
      const y1 = cy + Math.sin(this.angle) * start;
      const x2 = cx + Math.cos(this.angle) * (start + this.maxLen);
      const y2 = cy + Math.sin(this.angle) * (start + this.maxLen);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
      ctx.stroke();
      ctx.restore();
    }
  }
  
  export default {
    name: 'GreatingNotification',
    props: {
      message: { type: String, required: true },
      type:    { type: String, default: 'success' },
      duration:{ type: Number, default: 2000 }
    },
    setup(props) {
      const visible = ref(false);
      const canvasEl = ref(null);
      let ctx, w, h, particles = [], rays = [], animId;
      let lastTime = 0;
  
      async function initCanvas() {
        await nextTick();
        const canvas = canvasEl.value;
        if (!canvas) return;
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
        ctx = canvas.getContext('2d');
        rays = [];
        const countRays = 12;
        for (let i=0;i<countRays;i++) {
          rays.push(new Ray((2*Math.PI/countRays)*i, Math.max(w,h), 60 + i*5));
        }
      }
  
      function spawnParticles() {
        const count = 180;
        for (let i=0;i<count;i++) {
          const size = Math.random()*20+4;
          const speed = Math.random()*900+550;
          const angle = Math.random()*2*Math.PI;
          const x = w/2, y = h/2;
          const vx = Math.cos(angle)*speed;
          const vy = Math.sin(angle)*speed;
          const hue = Math.floor(Math.random()*60)+40;
          particles.push(new Particle(x,y,vx,vy,size,`hsl(${hue},70%,60%)`));
        }
      }
  
      function draw(dt) {
        ctx.clearRect(0,0,w,h);
        // radial bg
        const grad = ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,Math.max(w,h));
        grad.addColorStop(0, props.type==='success'?'#2ecc71':'#27ae60');
        grad.addColorStop(1, '#00000000'); ctx.fillStyle=grad; ctx.fillRect(0,0,w,h);
        // rays
        rays.forEach(r=>{r.update(dt);r.draw(ctx,w,h);});
        // particles
        particles = particles.filter(p=>p.life>0);
        particles.forEach(p=>(p.update(dt),p.draw(ctx)));
        // shimmer
        const sh = ctx.createLinearGradient(0,0,w,0);
        sh.addColorStop(0,'rgba(255,255,255,0)');sh.addColorStop(0.5,'rgba(255,255,255,0.08)');sh.addColorStop(1,'rgba(255,255,255,0)');
        ctx.fillStyle=sh; ctx.fillRect(0,0,w,h);
      }
  
      function animate(time) {
        const dt = (time-lastTime)/1000; lastTime=time;
        draw(dt);
        animId = requestAnimationFrame(animate);
      }
  
      function show() {
        visible.value=true; particles=[];
        initCanvas().then(()=>{ spawnParticles(); lastTime=performance.now(); animate(lastTime); });
        setTimeout(hide, props.duration);
      }
  
      function hide() { visible.value=false; cancelAnimationFrame(animId); particles=[]; rays=[]; }
  
      watch(()=>props.message, msg=>{ if(msg) show(); });
      onMounted(()=>{
            show();
          window.addEventListener('resize',initCanvas);
      })
      onUnmounted(()=>{ window.removeEventListener('resize',initCanvas); hide(); });
  
      return { visible, canvasEl };
    }
  };
  </script>
  
  <style scoped>
  .notification-root{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;pointer-events:none;}
  .notification-canvas{position:absolute;top:0;left:0;}
  .notification-content{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);padding:1rem 2rem;border-radius:6px;font-size:1.6rem;color:#fff;text-align:center;pointer-events:auto;}
  .notification-content.success{background:rgba(46,204,113,0.9);box-shadow:0 0 20px rgba(46,204,113,0.7);}
  .notification-content.error{background:rgba(231,76,60,0.9);box-shadow:0 0 20px rgba(231,76,60,0.7);}
  </style>
  