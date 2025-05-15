<template>
  <button :class="buttonClasses" @click="onClick" :disabled="isAnswered">
    {{ option.text }}
  </button>
</template>

<script>
export default {
  name: "OptionButton",
  props: {
    option: { type: Object, required: true },
    selected: { type: Boolean, default: false },
    isAnswered: { type: Boolean, default: false },
  },
  computed: {
    buttonClasses() {
      return {
        "option-btn": true,
        selected: this.selected,
        correct: this.selected && this.isAnswered && this.option.correct,
        incorrect: this.selected && this.isAnswered && !this.option.correct,
      };
    },
  },
  methods: {
    onClick() {
      if (!this.isAnswered) {
        this.$emit("select", this.option);
      }
    },
  },
};
</script>

<style scoped>
.option-btn {
  padding: 10px;
  background-color: #338bff;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
.option-btn:hover:not(.selected):not(.correct):not(.incorrect) {
  background-color: #7c716d;
}
.option-btn.selected.correct {
  background-color: #05ab68;
}
.option-btn.selected.incorrect {
  background-color: #ff3333;
}
.option-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
