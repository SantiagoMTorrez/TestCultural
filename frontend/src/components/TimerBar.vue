<template>
    <div class="timer-bar">
      <div :style="{ width: progress + '%' }"></div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TimerBar',
    props: {
      progress: {
        type: Number,
        required: true
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
    margin-bottom: 20px;
  }
  .timer-bar div {
    height: 100%;
    background-color: #2ecc71;
    transition: width 1s linear;
  }
  </style>
  