<!-- 用vuetify 加單選題 可打亂題目順序  -->
<template>
  <div class="quiz-page">
    <Header />
    <!-- 載入中畫面 - 當從心智圖頁面跳轉且正在等待題目生成時顯示 -->
    <div
      v-if="isLoading"
      class="loading-container mx-auto my-5 my-md-10 text-center"
    >
      <v-card
        class="pa-4 pa-md-6 elevation-3 mx-auto loading-card"
        max-width="95%"
        style="max-width: 500px; width: 100%"
      >
        <v-card-title class="text-h5 text-md-h4 mb-2 mb-md-4"
          >題目生成中</v-card-title
        >
        <v-card-text class="text-center">
          <v-progress-circular
            :size="60"
            :width="6"
            color="primary"
            indeterminate
            class="loading-spinner"
          ></v-progress-circular>
          <p class="text-subtitle-2 text-md-subtitle-1 mt-4 mt-md-6">
            正在為您生成測驗題目，請稍候...
          </p>
          <p class="text-body-2 text-grey mt-2">
            根據文件大小和複雜度，這可能需要幾秒鐘的時間。
          </p>
          <div class="loading-tips mt-4 mt-md-8 pa-3 pa-md-4">
            <p class="text-caption font-italic">
              提示：測驗完成後，您可以看到您的答題得分率，幫助您評估對內容的理解程度。
            </p>
          </div>
        </v-card-text>
      </v-card>
    </div>
    <!-- 歡迎信息 - 当没有问题数据且不在加載狀態時顯示 -->
    <div
      v-if="questions.length === 0 && !isLoading"
      class="no-data-container mx-auto my-5 my-md-10 text-center"
    >
      <v-card
        class="pa-4 pa-md-6 elevation-3 mx-auto"
        max-width="95%"
        style="max-width: 500px; width: 100%"
      >
        <v-card-title class="text-h5 text-md-h4 mb-2 mb-md-4"
          >歡迎來到測驗頁面</v-card-title
        >
        <v-card-text>
          <p class="text-subtitle-2 text-md-subtitle-1 mb-3 mb-md-6">
            您似乎是直接訪問此頁面，而沒有從心智圖頁面跳轉過來。
          </p>
          <p class="mb-4 mb-md-8">
            為了獲得測驗題目，請先前往心智圖頁面上傳 PDF 文件並生成心智圖，
            然後點擊「生成測驗」按鈕來創建針對該內容的測驗問題。
          </p>
          <v-btn
            color="primary"
            size="large"
            href="/mindmap"
            class="mt-2 mt-md-4"
          >
            前往心智圖頁面
          </v-btn>
        </v-card-text>
      </v-card>
    </div>
    <!-- 测验内容 - 当有问题数据且有当前问题且不在加載狀態時顯示 -->
    <div
      class="quiz-container mx-auto px-2 px-md-3 pt-2 overflow-hidden"
      v-if="questions.length > 0 && currentQuestion && !isLoading"
    >
      <!-- 標題 -->
      <div class="text-center mb-3 mb-md-4 mt-4 mt-md-6">
        <h2 class="text-h4 text-md-h3 font-bold text-primary mb-2">小測驗</h2>
      </div>
      <!-- 題目卡片 -->
      <v-card
        class="pa-3 pa-sm-4 pa-md-6 elevation-3 mx-auto question-card"
        max-width="95%"
      >
        <v-card-text>
          <div v-if="!quizFinished">
            <!-- 顯示目前題目 -->
            <h3
              class="text-subtitle-1 text-md-h6 font-weight-bold mb-3 mb-md-6"
            >
              {{ currentQuestionIndex + 1 }}. {{ currentQuestion.question }}
            </h3>

            <!-- 單選題處理 -->
            <div
              v-if="currentQuestion.type === 'single'"
              class="d-flex flex-column gap-3"
            >
              <v-btn
                v-for="(option, index) in currentQuestion.options"
                :key="`${index}-${currentQuestionIndex}`"
                class="justify-start text-left option-btn"
                variant="outlined"
                :disabled="showResult"
                :class="{
                  'text-grey':
                    showResult &&
                    index !== selectedAnswer &&
                    index !== currentQuestion.correct,
                  'text-error':
                    showResult &&
                    index === selectedAnswer &&
                    index !== currentQuestion.correct,
                  'text-success':
                    showResult && index === currentQuestion.correct,
                }"
                @click="handleSelectAnswer(index)"
              >
                <span class="option-text">{{ option }}</span>
                <v-icon
                  v-if="showResult && index === currentQuestion.correct"
                  color="green"
                  class="ml-2 result-icon"
                  >mdi-check</v-icon
                >
                <v-icon
                  v-if="
                    showResult &&
                    index === selectedAnswer &&
                    index !== currentQuestion.correct
                  "
                  color="red"
                  class="ml-2 result-icon"
                  >mdi-close</v-icon
                >
              </v-btn>
            </div>

            <!-- 是非題處理 -->
            <div
              v-else-if="currentQuestion.type === 'true-false'"
              class="d-flex flex-column gap-3"
            >
              <v-btn
                class="justify-start text-left option-btn"
                variant="outlined"
                :disabled="showResult"
                :class="{
                  'text-grey':
                    showResult &&
                    selectedAnswer !== null &&
                    selectedAnswer !== true &&
                    currentQuestion.correct !== true,
                  'text-success':
                    showResult && currentQuestion.correct === true,
                  'text-error':
                    showResult &&
                    selectedAnswer === true &&
                    currentQuestion.correct !== true,
                }"
                @click="handleSelectAnswer(true)"
              >
                <span class="option-text">𐤏</span
                ><!-- 勾勾：答對 -->
                <v-icon
                  v-if="showResult && currentQuestion.correct === true"
                  color="green"
                  class="ml-2 result-icon"
                  >mdi-check</v-icon
                >
                <!-- 叉叉：誤選 -->
                <v-icon
                  v-if="
                    showResult &&
                    selectedAnswer === true &&
                    currentQuestion.correct !== true
                  "
                  color="red"
                  class="ml-2 result-icon"
                  >mdi-close</v-icon
                >
              </v-btn>

              <v-btn
                class="justify-start text-left option-btn"
                variant="outlined"
                :disabled="showResult"
                :class="{
                  'text-grey':
                    showResult &&
                    selectedAnswer !== null &&
                    selectedAnswer !== false &&
                    currentQuestion.correct !== false,
                  'text-success':
                    showResult && currentQuestion.correct === false,
                  'text-error':
                    showResult &&
                    selectedAnswer === false &&
                    currentQuestion.correct !== false,
                }"
                @click="handleSelectAnswer(false)"
              >
                <span class="option-text">✕</span
                ><!-- 勾勾：答對 -->
                <v-icon
                  v-if="showResult && currentQuestion.correct === false"
                  color="green"
                  class="ml-2 result-icon"
                  >mdi-check</v-icon
                >
                <!-- 叉叉：誤選 -->
                <v-icon
                  v-if="
                    showResult &&
                    selectedAnswer === false &&
                    currentQuestion.correct !== false
                  "
                  color="red"
                  class="ml-2 result-icon"
                  >mdi-close</v-icon
                >
              </v-btn>
            </div>
            <!-- 答題結果顯示 -->
            <div v-if="showResult" class="text-center mt-4 mt-md-6">
              <p
                v-if="selectedAnswer === currentQuestion.correct"
                class="text-success font-weight-medium"
              >
                回答正確！
              </p>
              <p v-else class="text-error font-weight-medium">回答錯誤！</p>
              <v-btn class="mt-3 mt-md-4" color="primary" @click="nextQuestion"
                >下一題</v-btn
              >
            </div>
          </div>
          <!-- 測驗完成畫面 -->
          <div v-else class="text-center">
            <h3 class="text-h6 text-md-h5 font-weight-bold mb-3 mb-md-4">
              🎉 測驗完成
            </h3>
            <p class="text-subtitle-2 text-md-subtitle-1 mb-2">
              你答對了 {{ correctCount }} / {{ questions.length }} 題
            </p>
            <p class="text-grey">
              得分率：{{ Math.round((correctCount / questions.length) * 100) }}%
            </p>
            <div
              class="d-flex flex-column flex-sm-row justify-center mt-4 mt-md-6 button-container"
            >
              <v-btn
                color="indigo"
                class="mb-3 mb-sm-0 mx-sm-3"
                @click="restartQuiz"
                >重新開始</v-btn
              >
              <v-btn color="success" class="mx-sm-3" @click="regenerateQuiz"
                >重新生成新題目</v-btn
              >
            </div>
          </div>
        </v-card-text>
      </v-card>
      <!-- 下方進度條 -->
      <v-card
        class="mt-4 mt-md-6 py-2 progress-card"
        color="grey-lighten-3"
        flat
        tile
      >
        <v-card-text class="px-1 px-sm-2">
          <div class="text-center text-sm font-bold mb-2">
            {{ answeredCount }} / {{ questions.length }}
          </div>
          <div
            class="d-flex flex-column flex-sm-row align-center justify-space-between px-2 px-md-4 progress-container"
          >
            <span
              class="text-error font-weight-medium mb-2 mb-sm-0 progress-text"
            >
              錯誤：{{ incorrectCount }}
            </span>
            <v-progress-linear
              :key="progressPercentage"
              :model-value="progressPercentage"
              color="blue"
              height="10"
              rounded
              class="progress-bar mx-auto mx-sm-0"
            ></v-progress-linear>
            <span
              class="text-success font-weight-medium mt-2 mt-sm-0 progress-text"
            >
              正確：{{ correctCount }}
            </span>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <Footer />
  </div>
</template>

<script setup>
// Vue Composition API
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import Header from "@/views/AppHeader.vue";
import Footer from "@/views/AppFooter.vue";

// 狀態變數
const questions = ref([]);
const currentQuestionIndex = ref(0);
const selectedAnswer = ref(null);
const showResult = ref(false);
const correctCount = ref(0);
const incorrectCount = ref(0);
const answeredCount = ref(0);
const quizFinished = ref(false);
const isLoading = ref(false); // 加載狀態

// 計算目前題目與進度條
const currentQuestion = computed(
  () => questions.value[currentQuestionIndex.value]
);
const progressPercentage = computed(() =>
  Math.round((answeredCount.value / questions.value.length) * 100)
);

// 從API獲取問題
async function fetchQuestions(filename = null, jsonData = null) {
  try {
    // 如果沒有提供文件名或數據，則不發送請求，保持空問題列表以顯示歡迎頁面
    if (!filename && (!jsonData || Object.keys(jsonData).length === 0)) {
      console.log("未提供文件名或心智圖數據，顯示歡迎頁面");
      return;
    }

    // 設置加載狀態為 true
    isLoading.value = true;

    // 準備請求數據
    const requestData = {
      filename: filename || "",
      mindMapData: jsonData || {},
    };

    // 使用 POST 而不是 GET，並發送文件名和JSON數據
    const response = await axios.post("/api/quiz/questions", requestData);

    console.log("這是response", response);

    if (
      response.data.success &&
      response.data.questions &&
      response.data.questions.length > 0
    ) {
      questions.value = response.data.questions;
    } else {
      console.error("獲取問題失敗:", response.data.error || "沒有返回問題");
      // 如果沒有問題返回，保持問題列表為空，這樣會顯示歡迎頁面
    }
  } catch (error) {
    console.error("API請求錯誤:", error);
    if (error.code === "ERR_CONNECTION_REFUSED") {
      alert("無法連接到後端服務器，請確保後端服務器正在運行");
    } else {
      alert("獲取問題失敗，請稍後重試");
    }
  } finally {
    // 無論成功或失敗，都設置加載狀態為 false
    isLoading.value = false;
  }
}

// 初始化測驗
async function initQuiz() {
  // 檢查是否有從路由傳遞過來的參數
  const params = new URLSearchParams(window.location.search);
  const filename = params.get("filename");
  const jsonData = params.get("data");

  let parsedData = null;
  if (jsonData) {
    try {
      parsedData = JSON.parse(decodeURIComponent(jsonData));
    } catch (e) {
      console.error("解析心智圖數據失敗:", e);
    }
  } // 檢查是否從心智圖頁面正確跳轉過來
  const hasRequiredParams = filename || (jsonData && parsedData);

  if (hasRequiredParams) {
    await fetchQuestions(filename, parsedData);
  } else {
    console.log("直接訪問測驗頁面，顯示歡迎信息");
    // 保持 questions 為空數組，這樣會顯示歡迎頁面
  }
}

// 使用者點擊選項後的處理
function handleSelectAnswer(index) {
  if (!showResult.value) {
    selectedAnswer.value = index;
    showResult.value = true;
    const isCorrect = index === currentQuestion.value.correct;
    if (isCorrect) correctCount.value++;
    else incorrectCount.value++;
    answeredCount.value++;
  }
}

// 切換下一題
function nextQuestion() {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++;
    selectedAnswer.value = null;
    showResult.value = false;
  } else {
    quizFinished.value = true;
  }
}

// 重新開始測驗 - 使用現有題目
function restartQuiz() {
  currentQuestionIndex.value = 0;
  selectedAnswer.value = null;
  showResult.value = false;
  correctCount.value = 0;
  incorrectCount.value = 0;
  answeredCount.value = 0;
  quizFinished.value = false;
  // 不呼叫 initQuiz，直接重用現有題目
}

// 重新生成新題目
async function regenerateQuiz() {
  currentQuestionIndex.value = 0;
  selectedAnswer.value = null;
  showResult.value = false;
  correctCount.value = 0;
  incorrectCount.value = 0;
  answeredCount.value = 0;
  quizFinished.value = false;

  // 檢查是否有從路由傳遞過來的參數
  const params = new URLSearchParams(window.location.search);
  const filename = params.get("filename");
  const jsonData = params.get("data");

  let parsedData = null;
  if (jsonData) {
    try {
      parsedData = JSON.parse(decodeURIComponent(jsonData));
    } catch (e) {
      console.error("解析心智圖數據失敗:", e);
    }
  }

  // 重新獲取題目
  await fetchQuestions(filename, parsedData);
}

// 初始化時執行一次
onMounted(() => {
  initQuiz();
});
</script>

<style scoped>
/* 可加上背景樣式 */
body {
  background-color: #f5f7fa;
  overflow-x: hidden; /* 防止水平捲動 */
  width: 100%;
  max-width: 100vw;
}

.quiz-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden; /* 防止水平捲動 */
}

.quiz-container {
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden; /* 防止水平捲動 */
}

.no-data-container,
.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
}

.no-data-container .v-card,
.loading-container .v-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.no-data-container .v-card:hover,
.loading-container .v-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px);
}

/* 新增：統一選項按鈕樣式 */
.v-btn.option-btn {
  min-height: 50px !important; /* 較小設備的高度 */
  height: auto !important; /* 允許自適應高度 */
  width: 100%;
  max-width: 100%;
  white-space: normal;
  text-align: left;
  justify-content: flex-start;
  align-items: center;
  padding: 8px 12px;
  overflow: hidden;
  position: relative; /* 為絕對定位的圖標提供參考 */
  overflow-wrap: break-word;
  word-break: break-word;
  box-sizing: border-box;
}

@media (min-width: 600px) {
  .v-btn.option-btn {
    min-height: 60px !important; /* 大屏幕使用更高的高度 */
    padding: 12px 16px;
  }
}

/* 確保文本在按鈕內部正確換行 */
.option-text {
  display: block;
  width: calc(100% - 40px); /* 減去圖標的空間 */
  overflow-wrap: break-word;
  word-break: break-word;
  line-height: 1.4;
  font-size: 0.9rem;
  max-width: 100%;
}

@media (min-width: 600px) {
  .option-text {
    font-size: 1rem;
  }
}

/* 圖標靠右對齊 */
.result-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

/* 題目卡片高度與寬度 */
.question-card {
  min-height: 300px; /* 小設備較小高度 */
  height: auto; /* 允許自動擴展 */
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  overflow-x: hidden; /* 防止水平捲動 */
  box-sizing: border-box;
}

@media (min-width: 600px) {
  .question-card {
    min-height: 350px;
    width: 100% !important;
    max-width: 600px !important;
  }
}

@media (min-width: 960px) {
  .question-card {
    min-height: 400px;
    width: 100% !important;
    max-width: 800px !important;
  }
}

/* 確保卡片內容能夠填充高度 */
.question-card .v-card-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 載入中畫面的樣式 */
.loading-card {
  min-height: 280px;
  transition: all 0.5s ease;
}

@media (min-width: 600px) {
  .loading-card {
    min-height: 350px;
  }
}

.loading-spinner {
  animation: pulse 2s infinite;
}

/* 按鈕動畫效果 */
.v-btn {
  transition: all 0.3s ease;
}

/* 只在非觸控設備上顯示懸停效果 */
@media (hover: hover) {
  .v-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
}

/* 按鈕容器樣式 */
.button-container {
  gap: 16px;
}

@media (min-width: 600px) {
  .button-container {
    gap: 24px; /* 大屏幕上增加按鈕之間的間距 */
  }
}

.loading-tips {
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  border-left: 3px solid var(--v-primary-base);
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

/* 進度條樣式 */
.progress-bar {
  width: 100%;
  margin: 10px 0;
  max-width: 100%;
  overflow-x: hidden;
}

.progress-card {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

.progress-container {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

.progress-text {
  flex-shrink: 0;
}

/* 對所有容器增加通用防止溢出規則 */
[class*="container"],
[class*="card"],
.v-card,
.v-card-text {
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

@media (min-width: 600px) {
  .progress-bar {
    width: 60%;
    max-width: 60%;
    margin: 0;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
