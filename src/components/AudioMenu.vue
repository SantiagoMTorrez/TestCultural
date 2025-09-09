<template>
    <div class="audio-container">
      <!-- Botón de mute -->
      <button @click="toggleAudio" class="music-button">
        <span v-if="isPlaying">🔊</span>
        <span v-else>🔇</span>
      </button>
  
      <!-- Botón para mostrar control de volumen -->
      <button @click="toggleVolumeControl" class="volume-button">🎚️</button>
  
      <!-- Control de volumen -->
      <div v-if="showVolume" class="volume-control">
        <input type="range" min="0" max="1" step="0.01" v-model.number="volume" @input="changeVolume" />
      </div>
  
      <!-- Audio oculto -->
      <audio ref="audio" :src="require('@/assets/musicabo.mp3')" loop></audio>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AudioMenu',
    data() {
      return {
        isPlaying: false,
        volume: 0.5,
        showVolume: false
      };
    },
    mounted() {
      const audio = this.$refs.audio;
      audio.volume = this.volume;
      // ❌ No reproducimos automáticamente para evitar bloqueos
    },
    methods: {
      toggleAudio() {
        const audio = this.$refs.audio;
        if (this.isPlaying) {
          audio.pause();
          this.isPlaying = false;
        } else {
          audio.play().then(() => {
            this.isPlaying = true;
          }).catch(err => {
            console.warn("Error al intentar reproducir audio:", err);
          });
        }
      },
      toggleVolumeControl() {
        this.showVolume = !this.showVolume;
      },
      changeVolume() {
        this.$refs.audio.volume = this.volume;
      }
    }
  };
  </script>
  
  <style scoped>
  .audio-container {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
    background-color: #F7B787; /* color de la paleta */
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
  }
  
  .music-button,
  .volume-button {
    background: #EE7214; /* color de la paleta */
    border: none;
    font-size: 20px;
    color: white;
    cursor: pointer;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .volume-control input[type="range"] {
    width: 100px;
  }
  </style>
  