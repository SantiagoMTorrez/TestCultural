<template>
  <div class="quiz-container">
    <div class="quiz-card">
      <!-- Notificaciones de feedback -->
      <GreatingNotification v-if="showGreet" :message="greetMessage" />
      <FailedNotification   v-if="showFail"  :message="failMessage" />

      <div class="quiz-layout">
        <aside class="players-panel">
          <h3>Jugadores</h3>
          <ul>
            <li
              v-for="player in players"
              :key="player.id"
              :class="{ host: player.id === hostId }"
            >
              {{ player.username }} <span v-if="player.id === hostId">(Host)</span>
            </li>
          </ul>
          <button
            v-if="isHost && !sessionStarted"
            @click="startGame"
            class="start-btn"
          >Iniciar Partida</button>
        </aside>

        <section class="game-panel">
          <template v-if="!connected">
            <p class="loading">Conectando al juego...</p>
          </template>
          <template v-else-if="connected && !sessionStarted">
            <p class="waiting">Esperando a que el host inicie la partida...</p>
          </template>
          <template v-else>
            <!-- Barra de progreso -->
            <TimerBar :progress="questionTimerProgress" />
            <!-- Tarjeta de pregunta -->
            <div class="question-card">
              <p class="question-text">{{ question.text }}</p>
              <div class="options">
                <OptionButton
                  v-for="opt in options"
                  :key="opt.id"
                  :option="opt"
                  :selected="selectedOption === opt"
                  :isAnswered="answered"
                  @select="submitAnswer(opt.id)"
                />
              </div>
            </div>

            <div class="score-block">
              <p><strong>Puntuación:</strong> {{ score.toFixed(0) }}</p>
            </div>
          </template>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import TimerBar from './TimerBar.vue';
import OptionButton from './OptionButton.vue';
import GreatingNotification from './GreatingNotification.vue';
import FailedNotification from './FailedNotification.vue';

export default {
  name: 'GameQuiz',
  components: { TimerBar, OptionButton, GreatingNotification, FailedNotification },
  props: {
    testId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      socket: null,
      connected: false,
      question: {},
      options: [],
      totalQuestions: 0,
      startTs: 0,
      endTs: 0,
      timerInterval: null,
      remaining: 0,
      offset: 0,
      answered: false,
      selectedOption: null,
      score: 0,
      players: [],
      hostId: null,
      userId: null,
      sessionStarted: false,
      showGreet: false,
      greetMessage: '',
      showFail: false,
      failMessage: ''
    };
  },
  computed: {
    formattedTime() {
      const secs = Math.max(0, Math.ceil(this.remaining / 1000));
      const m = Math.floor(secs / 60);
      const s = secs % 60;
      return `${m}:${s < 10 ? '0' : ''}${s}`;
    },
    questionTimerProgress() {
      const duration = this.endTs - this.startTs;
      return duration > 0 ? (this.remaining / duration) * 100 : 0;
    },
    isHost() {
      return this.userId && this.hostId === this.userId;
    }
  },
  mounted() {
    this.userId = Number(localStorage.getItem('user_id'));
    const token = localStorage.getItem('token');
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const host = window.location.hostname;
    const port = '8080';
    const url = `${protocol}://${host}:${port}/ws/game/${this.testId}/?token=${token}`;
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      this.connected = true;
      this.socket.send(JSON.stringify({ action: 'time_sync' }));
    };
    this.socket.onmessage = ({ data }) => {
      const p = JSON.parse(data);
      switch (p.action) {
        case 'time_sync':
          this.offset = p.server_ts * 1000 - Date.now();
          break;
        case 'players_list':
          this.players = p.players;
          this.hostId = p.host_id;
          break;
        case 'question':
          this.sessionStarted = true;
          this.question = p.question;
          this.options = p.question.options;
          this.score = p.score ?? this.score;
          this.startTs = p.start_ts * 1000;
          this.endTs = p.end_ts * 1000;
          this.answered = false;
          this.selectedOption = null;
          clearInterval(this.timerInterval);
          this.timerInterval = setInterval(this.updateRemaining, 250);
          break;
        case 'update_score':
          this.score = p.score;
          break;
        case 'game_over':
          clearInterval(this.timerInterval);
          break;
      }
    };
    this.socket.onerror = err => console.error(err);
    this.socket.onclose = () => (this.connected = false);
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
    if (this.socket) this.socket.close();
  },
  methods: {
    updateRemaining() {
      const now = Date.now() + this.offset;
      this.remaining = this.endTs - now;
      if (this.remaining <= 0) clearInterval(this.timerInterval);
    },
    submitAnswer(id) {
      if (this.answered) return;
      this.socket.send(JSON.stringify({ action: 'submit', answer_id: id }));
      this.answered = true;
      this.selectedOption = this.options.find(o => o.id === id);
      // Notificaciones
      if (this.selectedOption.correct) {
        this.greetMessage = `¡Correcto! +${this.selectedOption.points ?? 0} pts`;
        this.showGreet = true;
        setTimeout(() => (this.showGreet = false), 1500);
      } else {
        this.failMessage = this.question.explanation || 'Incorrecto';
        this.showFail = true;
        setTimeout(() => (this.showFail = false), 1500);
      }
    },
    startGame() {
      if (this.isHost) {
        this.socket.send(JSON.stringify({ action: 'start' }));
        this.sessionStarted = true;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
.quiz-container {
  display: flex;
}
.quiz-card {
  background: rgba(255,255,255,0.95);
  border-radius: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 700px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  font-family: 'Jeju Hallasan', cursive;
}
.quiz-layout {
  display: flex;
}
.players-panel {
  width: 200px;
  background: #F9E8D9;
  padding: 1rem;
  border-radius: 8px;
  margin-right: 1rem;
}
.players-panel h3 {
  color: #527853;
  margin-top: 0;
}
.players-panel ul {
  list-style: none;
  padding: 0;
}
.players-panel li {
  padding: 0.5rem 0;
}
.players-panel li.host {
  font-weight: bold;
}
.players-panel .start-btn {
  width: 100%;
  padding: 0.5rem;
  margin-top: 1rem;
  background: #527853;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.players-panel .start-btn:hover {
  background: #3e6044;
}
.loading, .waiting {
  text-align: center;
  color: #555;
  margin: 2rem 0;
  font-style: italic;
}
.game-panel {
  flex: 1;
}
.question-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}
.question-text {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.score-block {
  text-align: right;
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
