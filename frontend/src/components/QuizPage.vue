<template>
  <div class="quiz-container">
    <h2>測驗</h2>
    <div v-if="loading">載入中...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="(question, index) in questions" :key="index" class="question-card">
        <h3>{{ question.question }}</h3>
        <div v-if="question.type === 'single'">
          <v-radio-group v-model="answers[index]">
            <v-radio
              v-for="(option, optIndex) in question.options"
              :key="optIndex"
              :label="option"
              :value="optIndex"
            ></v-radio>
          </v-radio-group>
        </div>
        <div v-else-if="question.type === 'true-false'">
          <v-radio-group v-model="answers[index]">
            <v-radio label="是" :value="true"></v-radio>
            <v-radio label="否" :value="false"></v-radio>
          </v-radio-group>
        </div>
      </div>
      <v-btn color="primary" @click="submitQuiz" :disabled="!isQuizComplete">
        提交答案
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'QuizPage',
  data() {
    return {
      questions: [],
      answers: {},
      loading: true,
      error: null,
      score: 0
    };
  },
  computed: {
    isQuizComplete() {
      return this.questions.length > 0 && 
             Object.keys(this.answers).length === this.questions.length;
    }
  },
  async created() {
    await this.fetchQuestions();
  },
  methods: {
    async fetchQuestions() {
      try {
        this.loading = true;
        this.error = null;
        const response = await axios.post('http://localhost:5001/api/quiz/generate');
        if (response.data.success) {
          this.questions = response.data.questions;
          // 初始化答案對象
          this.questions.forEach((_, index) => {
            this.answers[index] = null;
          });
        } else {
          throw new Error(response.data.error || '獲取題目失敗');
        }
      } catch (error) {
        console.error('API請求錯誤:', error);
        this.error = '獲取題目失敗，請稍後重試';
      } finally {
        this.loading = false;
      }
    },
    submitQuiz() {
      let correctAnswers = 0;
      this.questions.forEach((question, index) => {
        if (this.answers[index] === question.correct) {
          correctAnswers++;
        }
      });
      this.score = (correctAnswers / this.questions.length) * 100;
      alert(`測驗完成！得分：${this.score}%`);
    }
  }
};
</script>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.question-card {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
}

h3 {
  margin-bottom: 15px;
}
</style> 