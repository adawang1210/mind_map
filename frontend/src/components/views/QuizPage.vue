<!-- 用vuetify 加單選題 可打亂題目順序  -->
<template>
  <div class="container mx-auto px-0 pt-2 max-w-full" v-if="currentQuestion">
    <!-- 標題 -->
    <div class="text-center mb-4">
      <h2 class="text-4xl font-bold text-primary mb-2">小測驗</h2>
    </div>

    <!-- 題目卡片 -->
    <v-card class="pa-6 elevation-3 mx-auto" max-width="80%">
      <v-card-text>
        <div v-if="!quizFinished">
          <!-- 顯示目前題目 -->
          <h3 class="text-h6 font-weight-bold mb-6">
            {{ currentQuestionIndex + 1 }}. {{ currentQuestion.question }}
          </h3>

          <!-- 單選題處理 -->
          <div v-if="currentQuestion.type === 'single'" class="d-flex flex-column gap-3">
            <v-btn
              v-for="(option, index) in currentQuestion.options"
              :key="`${index}-${currentQuestionIndex}`"
              class="justify-start text-left"
              variant="outlined"
              :disabled="showResult"
              :class="{
                'text-grey': showResult && index !== selectedAnswer && index !== currentQuestion.correct,
                'text-error': showResult && index === selectedAnswer && index !== currentQuestion.correct,
                'text-success': showResult && index === currentQuestion.correct
              }"
              @click="handleSelectAnswer(index)"
            >
              {{ option }}
              <v-icon
                v-if="showResult && index === currentQuestion.correct"
                color="green"
                class="ml-2"
              >mdi-check</v-icon>
              <v-icon
                v-if="showResult && index === selectedAnswer && index !== currentQuestion.correct"
                color="red"
                class="ml-2"
              >mdi-close</v-icon>
            </v-btn>
          </div>

          <!-- 是非題處理 -->
          <div v-else-if="currentQuestion.type === 'true-false'" class="d-flex flex-column gap-3">
            <v-btn
              class="justify-start text-left"
              variant="outlined"
              :disabled="showResult"
              :class="{
                'text-grey': showResult && selectedAnswer !== null && selectedAnswer !== true && currentQuestion.correct !== true,
                'text-success': showResult && currentQuestion.correct === true,
                'text-error': showResult && selectedAnswer === true && currentQuestion.correct !== true
              }"
              @click="handleSelectAnswer(true)"
            >
              𐤏          
              <!-- 勾勾：答對 -->
              <v-icon
                v-if="showResult && currentQuestion.correct === true"
                color="green"
                class="ml-2"
              >mdi-check</v-icon>
              <!-- 叉叉：誤選 -->
              <v-icon
                v-if="showResult && selectedAnswer === true && currentQuestion.correct !== true"
                color="red"
                class="ml-2"
              >mdi-close</v-icon>
            </v-btn>

            <v-btn
              class="justify-start text-left"
              variant="outlined"
              :disabled="showResult"
              :class="{
                'text-grey': showResult && selectedAnswer !== null && selectedAnswer !== false && currentQuestion.correct !== false,
                'text-success': showResult && currentQuestion.correct === false,
                'text-error': showResult && selectedAnswer === false && currentQuestion.correct !== false
              }"
              @click="handleSelectAnswer(false)"
            >
              ✕
              <!-- 勾勾：答對 -->
              <v-icon
                v-if="showResult && currentQuestion.correct === false"
                color="green"
                class="ml-2"
              >mdi-check</v-icon>
              <!-- 叉叉：誤選 -->
              <v-icon
                v-if="showResult && selectedAnswer === false && currentQuestion.correct !== false"
                color="red"
                class="ml-2"
              >mdi-close</v-icon>
            </v-btn>
          </div>

          <!-- 答題結果顯示 -->
          <div v-if="showResult" class="text-center mt-6">
            <p v-if="selectedAnswer === currentQuestion.correct" class="text-success font-weight-medium">回答正確！</p>
            <p v-else class="text-error font-weight-medium">回答錯誤！</p>
            <v-btn class="mt-4" color="primary" @click="nextQuestion">下一題</v-btn>
          </div>
        </div>

        <!-- 測驗完成畫面 -->
        <div v-else class="text-center">
          <h3 class="text-h5 font-weight-bold mb-4">🎉 測驗完成</h3>
          <p class="text-subtitle-1 mb-2">你答對了 {{ correctCount }} / {{ questions.length }} 題</p>
          <p class="text-grey">得分率：{{ Math.round((correctCount / questions.length) * 100) }}%</p>
          <v-btn class="mt-6" color="indigo" @click="restartQuiz">重新開始</v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- 下方進度條 -->
    <v-card class="mt-6 px-0 py-2" color="grey-lighten-3" flat tile>
      <v-card-text class="px-0">
        <div class="text-center text-sm font-bold mb-2">
          {{ answeredCount }} / {{ questions.length }}
        </div>
        <div class="d-flex align-center justify-space-between px-4">
          <span class="text-error font-weight-medium">錯誤：{{ incorrectCount }}</span>
          <v-progress-linear
            :key="progressPercentage"
            :model-value="progressPercentage"
            color="blue"
            height="10"
            rounded
            style="width: 75%"
          ></v-progress-linear>
          <span class="text-success font-weight-medium">正確：{{ correctCount }}</span>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
// Vue Composition API
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// 狀態變數
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const showResult = ref(false)
const correctCount = ref(0)
const incorrectCount = ref(0)
const answeredCount = ref(0)
const quizFinished = ref(false)

// 計算目前題目與進度條
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const progressPercentage = computed(() => Math.round((answeredCount.value / questions.value.length) * 100))

// 從API獲取問題
async function fetchQuestions() {
  try {
    const response = await axios.get('/api/quiz/questions')


    console.log("這是response", response)

    if (response.data.success) {
      questions.value = response.data.questions
    } else {
      console.error('獲取問題失敗:', response.data.error)
      alert('獲取問題失敗，請稍後重試')
    }
  } catch (error) {
    console.error('API請求錯誤:', error)
    if (error.code === 'ERR_CONNECTION_REFUSED') {
      alert('無法連接到後端服務器，請確保後端服務器正在運行')
    } else {
      alert('獲取問題失敗，請稍後重試')
    }
  }
}

// 初始化測驗
async function initQuiz() {
  await fetchQuestions()
}

// 使用者點擊選項後的處理
function handleSelectAnswer(index) {
  if (!showResult.value) {
    selectedAnswer.value = index
    showResult.value = true
    const isCorrect = index === currentQuestion.value.correct
    if (isCorrect) correctCount.value++
    else incorrectCount.value++
    answeredCount.value++
  }
}

// 切換下一題
function nextQuestion() {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedAnswer.value = null
    showResult.value = false
  } else {
    quizFinished.value = true
  }
}

// 重新開始測驗
function restartQuiz() {
  currentQuestionIndex.value = 0
  selectedAnswer.value = null
  showResult.value = false
  correctCount.value = 0
  incorrectCount.value = 0
  answeredCount.value = 0
  quizFinished.value = false
  initQuiz()
}

// 初始化時執行一次
onMounted(() => {
  initQuiz()
})
</script>

<style scoped>
/* 可加上背景樣式 */
body {
  background-color: #f5f7fa;
}
</style>




