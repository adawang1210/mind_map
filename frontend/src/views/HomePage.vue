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

  <!--預設主題-->
  <section class="themes-section">
        <h2 class="section-title">預設主題</h2>
        <div class="themes-container">
            
                <div class="theme-card">
                    <div class="theme-image">
                        <img src="../assets/French-Revolution.webp" alt="法國大革命" />
                    </div>
                    <div class="theme-content">
                        <h3 class="theme-title">法國大革命</h3>
                        <p class="theme-description">探索1789年至1799年間改變法國歷史進程的重大事件</p>
                    </div>
                </div>
            
            <div class="theme-card">
                <div class="theme-image">
                    <img src="../assets/Mai68_StudentMovement.webp" alt="68學運 / 五月風暴 Mai 68" />
                </div>
                <div class="theme-content">
                    <h3 class="theme-title">68學運 / 五月風暴 Mai 68</h3>
                    <p class="theme-description">1968年五月，學生與工人走上街頭，記錄了法國社會動盪的轉捩點</p>
                </div>
            </div>

            <div class="theme-card">
                <div class="theme-image">
                    <img src="../assets/The-Hundred-Years-War.webp" alt="百年戰爭" />
                </div>
                <div class="theme-content">
                    <h3 class="theme-title">百年戰爭</h3>
                    <p class="theme-description">英格蘭與法國之間為爭奪法國王位及領土而爆發的長期衝突，最終法國獲勝，並強化了民族認同。</p>
                </div>
            </div>
        </div>
  </section>
  
  <!--心智圖共享市集-->
  <section class="themes-section">
        <h2 class="section-title">心智圖共享市集</h2>
        <div class="themes-container">
            
                <div class="theme-card">
                    <div class="theme-image">
                        <img src="../assets/Commune-de-Paris.jpeg" alt="巴黎公社" />
                    </div>
                    <div class="theme-content">
                        <h3 class="theme-title">巴黎公社</h3>
                        <p class="theme-description">世界上第一個無產階級政權</p>
                    </div>
                </div>
            
            <div class="theme-card">
                <div class="theme-image">
                    <img src="../assets/普法戰爭.jpeg" alt="普法戰爭" />
                </div>
                <div class="theme-content">
                    <h3 class="theme-title">普法戰爭</h3>
                    <p class="theme-description">法國與普魯士之間的戰爭，導致法國戰敗、拿破崙三世下台，並促成德意志帝國的統一。</p>
                </div>
            </div>

            <div class="theme-card">
                <div class="theme-image">
                    <img src="../assets/阿爾及利亞獨立戰爭.jpeg" alt="阿爾及利亞獨立戰爭" />
                </div>
                <div class="theme-content">
                    <h3 class="theme-title">阿爾及利亞獨立戰爭</h3>
                    <p class="theme-description">法國與阿爾及利亞民族解放陣線之間的血腥衝突，最終導致阿爾及利亞脫離法國殖民統治、取得獨立。</p>
                </div>
            </div>
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
    background-image: url('../assets/french-history-bg.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    width: 100%;
    min-height: 500px;
    max-height: 1080px;
    display: flex;
    align-items: center;
    justify-content: center;
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

/* Themes Section */
.themes-section {
    padding: 5rem 0;
    background-color: #fff;
    text-align: center;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 2.5rem;
    text-align: center;
    position: relative;
}

.section-title:after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background-color: #2563eb;
    border-radius: 2px;
}

.themes-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px;
}

.theme-card {
    background-color: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.theme-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.theme-image {
    height: 220px;
    overflow: hidden;
}

.theme-image img {
    width: 100%;
    height: 100%;
    object-fit: fill;
    transition: transform 0.5s ease;
}

.theme-card:hover .theme-image img {
    transform: scale(1.05);
}

.theme-content {
    padding: 1.5rem;
    text-align: left;
}

.theme-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.75rem;
}

.theme-description {
    font-size: 1rem;
    color: #6b7280;
    line-height: 1.5;
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
    
    .section-title {
        font-size: 2rem;
    }
    
    .theme-image {
        height: 180px;
    }
    
    .theme-title {
        font-size: 1.25rem;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .theme-card {
        max-width: 320px;
        margin: 0 auto;
    }
}

/* 添加媒体查询以适应不同屏幕 */
@media screen and (max-width: 768px) {
    .hero-section {
        height: 80vh;
        min-height: 400px;
    }
}

@media screen and (max-width: 480px) {
    .hero-section {
        height: 70vh;
        min-height: 300px;
    }
}
</style>