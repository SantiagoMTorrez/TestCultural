<template>
  <div class="container">
    <div class="card">
      <h2 class="card-title">INGRESE UNA NUEVA PREGUNTA</h2>
      <form @submit.prevent="registrar">
        <div class="form-group">
          <label>Elija una categoría</label>
          <select v-model="selectedCategory" class="input-control" required>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Pregunta</label>
          <input v-model="pregunta" type="text" class="input-control" required />
        </div>

        <div class="form-group">
          <label>Explicación</label>
          <input v-model="explicacion" type="text" class="input-control" required />
        </div>

        <div class="form-group">
          <label>Dificultad</label>
          <select v-model="dificultad" class="input-control" required>
            <option value="Fácil">Fácil</option>
            <option value="Medio">Medio</option>
            <option value="Difícil">Difícil</option>
          </select>
        </div>

        <div class="form-group">
          <label>Opciones de respuesta</label>
          <p class="hint">Haga clic en el círculo rojo para marcar la respuesta correcta</p>
          <div class="answers-list">
            <div v-for="(ans, idx) in answers" :key="idx" class="answer-item">
              <span
                class="answer-marker"
                :class="{ selected: ans.correct }"
                @click="markCorrect(idx)"
                title="Marcar como correcta"
              ></span>
              <input
                v-model="ans.text"
                type="text"
                class="input-control answer-input"
                placeholder="Texto de la respuesta"
                required
              />
              <button
                type="button"
                class="btn-delete"
                @click="removeAnswer(idx)"
                :disabled="answers.length <= 2"
                title="Eliminar opción"
              >&times;</button>
            </div>
            <button type="button" class="btn-add" @click="addAnswer">+ Agregar opción</button>
          </div>
        </div>

        <div class="actions">
          <button type="submit" class="btn-primary">Registrar</button>
          <button type="button" class="btn-secondary" @click="salir">Salir</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'NuevaPreguntas',
  setup() {
    const router = useRouter();
    const categories = ref([]);
    const selectedCategory = ref(null);
    const pregunta = ref('');
    const explicacion = ref('');
    const dificultad = ref('Fácil');
    const answers = ref([
      { text: '', correct: true },
      { text: '', correct: false }
    ]);

    onMounted(async () => {
      const token = localStorage.getItem('token');
      try {
        const res = await fetch(`http://${window.location.hostname}:8080/trivia/categories/`, {
          headers: { accept: 'application/json', Authorization: `Token ${token}` }
        });
        if (res.ok) categories.value = await res.json();
      } catch(e) {
        console.error('Error cargando categorías', e);
      }
    });

    const addAnswer = () => {
      answers.value.push({ text: '', correct: false });
    };

    const removeAnswer = (index) => {
      if (answers.value.length > 2) {
        const wasCorrect = answers.value[index].correct;
        answers.value.splice(index, 1);
        if (wasCorrect && !answers.value.some(a => a.correct)) {
          answers.value[0].correct = true;
        }
      }
    };

    const markCorrect = (index) => {
      answers.value.forEach((ans, i) => ans.correct = (i === index));
    };

    const registrar = async () => {
      if (!answers.value.some(a => a.correct)) {
        alert('Debe marcar al menos una respuesta como correcta.');
        return;
      }
      const diffMap = { 'Fácil': 1, 'Medio': 2, 'Difícil': 3 };
      const difficultyFK = diffMap[dificultad.value] || 1;
      const score = 10 * difficultyFK;
      const payload = {
        text: pregunta.value,
        explanation: explicacion.value,
        difficulty: difficultyFK,
        score,
        category: selectedCategory.value,
        question_type: 1,
        answer_options: answers.value.map(a => ({ text: a.text, correct: a.correct }))
      };
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(
          `http://${window.location.hostname}:8080/trivia/questions/create/`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Authorization: `Token ${token}` },
            body: JSON.stringify(payload)
          }
        );
        if (res.ok) {
          alert('Pregunta registrada correctamente');
          router.push('/staffMain');
        } else {
          const err = await res.json();
          alert(err.message || 'Error al registrar');
        }
      } catch(e) {
        console.error(e);
        alert('Error de conexión');
      }
    };

    const salir = () => router.push('/staffMain');

    return {
      categories,
      selectedCategory,
      pregunta,
      explicacion,
      dificultad,
      answers,
      addAnswer,
      removeAnswer,
      markCorrect,
      registrar,
      salir
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lexend+Giga&display=swap');

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: black;
  padding: 1rem;
}

.card {
  background: var(--c-panel);
  padding: 2rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  width: 100%;
  max-width: 600px;
}

.card-title {
  text-align: center;
  color: var(--c-primary);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-group { margin-bottom: 1rem; }
.input-control { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: var(--radius); font-size: 1rem; }

.answers-list { display: flex; flex-direction: column; gap: 0.5rem; }
.answer-item { display: flex; align-items: center; gap: 0.5rem; }
.answer-marker { width: 1rem; height: 1rem; border: 2px solid var(--c-error); border-radius: 50%; cursor: pointer; }
.answer-marker.selected { background: var(--c-error); }
.answer-input { flex: 1; }

.btn-delete { background: transparent; border: none; color: var(--c-error); font-size: 1.2rem; cursor: pointer; padding: 0; }
.btn-delete:disabled { color: #ccc; cursor: not-allowed; }

.btn-add { align-self: start; background: transparent; border: 2px dashed var(--c-primary); border-radius: var(--radius); color: var(--c-primary); padding: 0.5rem 1rem; cursor: pointer; transition: background 0.3s; }
.btn-add:hover { background: var(--c-secondary); color: #fff; }

.actions { display: flex; gap: 1rem; margin-top: 1.5rem; }
.btn-primary, .btn-secondary { flex: 1; padding: 0.75rem; border: none; border-radius: var(--radius); cursor: pointer; font-size: 1rem; color: #fff; transition: background 0.3s; }
.btn-primary { background: var(--c-primary); }
.btn-primary:hover { background: var(--c-secondary); }
.btn-secondary { background: var(--c-error); }
.btn-secondary:hover { background: #a62828; }

.hint { font-size: 0.85rem; color: var(--c-text); margin-bottom: 0.5rem; }
</style>