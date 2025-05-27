<template>
  <Header />

  <section class="hero-section">
    <div class="overlay"></div>
    <div class="hero-content">
      <h1 class="hero-title">法國歷史全覽圖</h1>
      <p class="hero-subtitle">破解原文，一圖讀懂</p>
      <a href="/mindmap">
        <button class="cta-button">開始!</button>
      </a>
    </div>
  </section>

  <section class="features-section">
    <div class="features-container">
      <div class="feature-card">
        <h3 class="feature-title">🧠自動生成心智圖</h3>
        <ul class="feature-list">
          <li>上傳PDF</li>
          <li>智能提取關鍵詞</li>
          <li>快速生成可編輯心智圖</li>
        </ul>
      </div>

      <div class="feature-card">
        <h3 class="feature-title">✏️互動編輯與匯出</h3>
        <ul class="feature-list">
          <li>自由編輯心智圖</li>
          <li>輕鬆添加刪除節點</li>
          <li>一鍵匯出高品質PNG</li>
        </ul>
      </div>

      <div class="feature-card">
        <h3 class="feature-title">❓智能測驗助學習</h3>
        <ul class="feature-list">
          <li>定制小測驗</li>
          <li>檢驗歷史知識掌握</li>
          <li>鞏固學習成果</li>
        </ul>
      </div>
    </div>
  </section>

  <Footer />
</template>

<script setup>
import Header from "./AppHeader.vue";
import Footer from "./AppFooter.vue";
</script>

<style scoped>
/* Hero Section */
.hero-section {
  position: relative;
  background-image: url("../assets/french-history-bg.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  width: 100%;
}

.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.4);
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #fff;
  padding: 0 16px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.1em;
}

.hero-subtitle {
  font-size: 1.75rem;
  font-weight: 700;
  max-width: 48rem;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.05em;
}

.cta-button {
  background-color: #2563eb;
  color: #fff;
  font-size: 1.25rem;
  font-weight: 600;
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 9999px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.cta-button:hover {
  background-color: #1e40af;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* Features Section */
.features-section {
  padding: 4rem 0;
  background-color: #f3f4f6;
  text-align: center;
}

.features-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1024px;
  margin: 0 auto;
  padding: 0 16px;
}

.feature-card {
  background-color: #ededed;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2563eb;
  margin-bottom: 0.75rem;
  text-decoration: underline;
}

.feature-list {
  text-align: left;
  color: #4b5563;
  list-style: disc inside;
  line-height: 1.75;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }

  .hero-subtitle {
    font-size: 1.5rem;
  }

  .cta-button {
    font-size: 1rem;
    padding: 0.75rem 2rem;
  }
}
</style>
