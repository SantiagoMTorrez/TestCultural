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
              <div class="player-info">
                <span v-if="player.id === hostId" class="host-label">Host</span>
                <span class="player-name">{{ player.username }}</span>
                <span class="player-score">{{ Math.round(player.score) }}</span>
              </div>
            </li>
          </ul>
          <button
          v-if="isHost && !sessionStarted && !gameOver"
          @click="startGame"
          class="start-btn"
          >Iniciar Partida</button>
        </aside>
        
        <section class="game-panel">
          <!-- Estado de conexión y espera -->
          <div v-if="!connected" class="status-message">Conectando al juego...</div>
          <div v-else-if="gameOver" class="summary-board">
            <h2>Resumen del Juego</h2>
            <ul>
              <li
                v-for="player in summaryPlayers"
                :key="player.id"
                :class="{ winner: player.id === summaryPlayers[0].id }"
              >
                <div class="player-info">
                  <span class="summary-name">{{ player.username }}</span>
                  <span class="summary-score">{{ Math.round(player.score) }}</span>
                </div>
              </li>
            </ul>
            <div style="width: 100%; display: flex; justify-content: center; padding: 1rem;">
              <OptionButton
                :option="{text: 'Regresar'}"
                @select="handleSelect"
              />
            </div>
          </div>
          <div v-else-if="connected && !sessionStarted && !countDown" class="status-message">Esperando a que el host inicie la partida...</div>
          <!-- Cuenta regresiva -->
          <div v-else-if="connected && countDown" class="count_down_container">
            <div class="count_down_circle"> 
              <p>{{ counter }}</p>
            </div>
          </div>
          <!-- Resumen de juego al finalizar -->
          <!-- Lógica de preguntas durante la partida -->
          <div v-else class="question-panel">
            <!-- Barra de progreso -->
            <TimerBar :duration="questionDuration" :reverse="true" />
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
          </div>
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
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'GameQuiz',
  components: { TimerBar, OptionButton, GreatingNotification, FailedNotification },
  props: {
    testId: { type: [String, Number], required: true }
  },
  data() {
    return {
      router:  useRouter(),
      route: useRoute(),
      socket: null,
      connected: false,
      countDown: false,
      counter: 0,
      question: {},
      options: [],
      startTs: 0,
      endTs: 0,
      answered: false,
      selectedOption: null,
      score: 0,
      players: [],
      hostId: null,
      userId: null,
      sessionStarted: false,
      gameOver: false,
      summaryPlayers: [],
      showGreet: false,
      greetMessage: '',
      showFail: false,
      failMessage: '',
      questionDuration: 0,
    };
  },
  computed: {
    isHost() { return this.userId && this.hostId === this.userId; }
  },
  mounted() {
    this.userId = Number(localStorage.getItem('user_id'));
    const token = localStorage.getItem('token');
    const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${protocol}://${location.hostname}:8080/ws/game/${this.testId}/?token=${token}`;
    this.socket = new WebSocket(url);
    this.socket.onopen = () => {
      this.connected = true;
      this.socket.send(JSON.stringify({ action: 'time_sync' }));
    };
    this.socket.onmessage = ({ data }) => {
      const p = JSON.parse(data);
      switch (p.action) {
        case 'time_sync': this.offset = p.server_ts*1000-Date.now(); break;
        case 'players_list': this.players=p.players; this.hostId=p.host_id; break;
        case 'question':
          this.countDown=false; this.sessionStarted=true;
          this.question=p.question; this.options=p.question.options;
          this.score=p.score||this.score;
          this.startTs=p.start_ts; this.endTs=p.end_ts;
          this.questionDuration=this.endTs-this.startTs;
          this.answered=false; this.selectedOption=null;
          break;
          case 'counter': this.countDown=true; this.counter=p.index; break;
          case 'update_score': 
          
            this.score=p.score; break;
          case 'game_over':
            this.gameOver=true;
            this.summaryPlayers=[...this.players].sort((a,b)=>b.score-a.score);
            if(this.summaryPlayers[0].id == this.userId){              
              this.greetMessage=`¡Ganaste!`;
              this.showGreet = true;
              setTimeout(() => {this.showGreet = false}, 1500)
            }
          break;
      }
    };
    this.socket.onerror=console.error;
    this.socket.onclose=()=>this.connected=false;
  },
  beforeUnmount() {
    if (this.socket) this.socket.close();
  },
  methods:{
    handleSelect(){
      this.router.go(-1)
    },
    submitAnswer(id){
      if(this.answered) return;
      this.socket.send(JSON.stringify({action:'submit',answer_id:id}));
      this.answered=true;
      this.selectedOption=this.options.find(o=>o.id===id);
      if(this.selectedOption.correct){
        this.greetMessage=`¡Correcto! +${this.selectedOption.points||0} pts`;
        this.showGreet=true; setTimeout(()=>this.showGreet=false,1500);
      } else {
        this.failMessage=this.question.explanation||'Incorrecto';
        this.showFail=true; setTimeout(()=>this.showFail=false,1500);
      }
    },
    startGame(){ if(this.isHost){ this.socket.send(JSON.stringify({action:'start'})); this.sessionStarted=true; }}
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jeju+Hallasan&display=swap');
.quiz-container{display:flex;justify-content:center;align-items:center;padding:1rem;box-sizing:border-box;height:100%;}
.quiz-card{background:rgba(255,255,255,0.98);border-radius:1rem;padding:1.5rem;max-width:1200px;width:100%;box-shadow:0 2px 4px rgba(0,0,0,0.1);font-family:'Jeju Hallasan',cursive;}
.quiz-layout{display:grid;grid-template-columns:1fr 2fr;gap:1rem;}
.players-panel{background:#F9E8D9;padding:1rem;border-radius:0.75rem;display:flex;flex-direction:column;}
.players-panel h3{margin:0 0 0.5rem;color:#527853;}
.players-panel ul{list-style:none;padding:0;flex:1;overflow:auto;}
.players-panel li{margin-bottom:0.5rem;}
.player-info{display:flex;justify-content:space-between;align-items:center;}
.host-label{background:#527853;color:#fff;padding:0.2rem 0.4rem;border-radius:0.25rem;font-size:0.75rem;}
.player-name{flex:1;margin-left:0.5rem;}
.player-score{font-weight:bold;}
.start-btn{margin-top:0.5rem;padding:0.5rem;border:none;border-radius:0.5rem;background:#527853;color:#fff;cursor:pointer;transition:background 0.2s;}
.start-btn:hover{background:#3e6044;}
.game-panel{background:#fff;border-radius:0.75rem;padding:1rem;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:300px;}
.status-message{font-style:italic;color:#555;margin:2rem 0;}
.count_down_container{display:flex;justify-content:center;align-items:center;width:100%;flex:1;}
.count_down_circle{display:flex;justify-content:center;align-items:center;border-radius:50%;width:8rem;height:8rem;background:#333;color:#fff;font-size:2rem;}
.summary-board{width:100%;}
.summary-board h2{text-align:center;margin-bottom:1rem;}
.summary-board ul{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0.5rem;}
.summary-board li{background:#F9E8D9;padding:0.75rem;border-radius:0.5rem;text-align:center;}
.summary-board li.winner{background:#527853;color:#fff;font-weight:bold;}
.question-panel{width:100%;}
.question-card{background:#f9f9f9;padding:1rem;border-radius:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,0.1);margin-bottom:1rem;}
.question-text{font-size:1.25rem;margin-bottom:0.75rem;}
.options{display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;}
.score-block{text-align:right;font-size:1.1rem;font-weight:bold;}
/* Responsive */
@media(max-width:768px){
  .quiz-layout{grid-template-columns:1fr;}
  .options{grid-template-columns:1fr;}
  .summary-board ul{grid-template-columns:1fr;}
}
</style>