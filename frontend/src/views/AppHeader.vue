<template>
  <header class="header">
    <div class="logo">法國歷史全覽圖</div>
    <!-- 漢堡按鈕（只在小螢幕顯示） -->
    <div class="hamburger" @click="toggleMenu" :class="{ active: menuOpen }">
      <img src="@/assets/hamburger.png" alt="Menu" class="hamburger-icon" />
    </div>
    <!-- 導航菜單 -->
    <nav class="nav" :class="{ 'nav-open': menuOpen }">
      <ul>
        <li>
          <router-link to="/homepage" @click="closeMenu">首頁</router-link>
        </li>
        <li>
          <router-link to="/mindmap" @click="closeMenu">心智圖</router-link>
        </li>
        <li>
          <router-link to="/quizpage" @click="closeMenu">小測驗</router-link>
        </li>
      </ul>
    </nav>
    <!-- 背景遮罩，只在移動端菜單打開時顯示 -->
    <div class="menu-overlay" v-if="menuOpen" @click="closeMenu"></div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      menuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    closeMenu() {
      this.menuOpen = false;
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  overflow-x: hidden; /* 防止水平滾動 */
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* 讓 logo 靠左，nav 靠右 */
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  padding: 12px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1000; /* 確保下拉選單顯示在其他內容上方 */
  width: 100%;
  box-sizing: border-box;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-right: 30px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1; /* 允許在空間不足時縮小 */
}

/* 漢堡按鈕樣式 */
.hamburger {
  display: none; /* 預設隱藏 */
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1010;
  padding: 8px;
  transition: transform 0.3s ease;
  position: relative;
}

.hamburger-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

/* 漢堡按鈕動畫效果（當菜單打開時） */
.hamburger.active .hamburger-icon {
  transform: rotate(90deg);
}

/* 遮罩層 */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: none;
}

.nav {
  display: flex;
  align-items: center;
}

.nav ul {
  list-style: none;
  margin: 0;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.nav li {
  margin: 0 1.5rem;
}

.nav a {
  text-decoration: none;
  color: #666;
  font-size: 16px;
  display: flex;
  align-items: center;
  transition: color 0.2s ease, background-color 0.2s ease;
  padding: 10px 0;
  position: relative;
}

.nav a.router-link-active {
  color: #007bff;
}

.nav a:hover {
  color: #007bff;
}

/* 添加圖標樣式 */
.nav a::before {
  display: inline-block;
  width: 1em;
  margin-right: 8px;
  font-size: 1.1em;
  transition: transform 0.2s ease;
}

/* 為每個導航項添加特定圖標 */
.nav li:nth-child(1) a::before {
  /* 首頁 */
  content: "🏠";
}

.nav li:nth-child(2) a::before {
  /* 心智圖 */
  content: "🧠";
}

.nav li:nth-child(3) a::before {
  /* 小測驗 */
  content: "📝";
}

.nav a:hover::before {
  transform: scale(1.1);
}

/* 平板和移動設備的響應式設計 */
@media (max-width: 768px) {
  .logo {
    font-size: 20px; /* 較小的 logo 文字 */
    max-width: calc(100% - 50px); /* 為漢堡按鈕預留空間 */
  } /* 顯示漢堡按鈕 */
  .hamburger {
    display: flex !important; /* 強制顯示 */
    align-items: center;
    justify-content: center;
  }

  /* 顯示遮罩層 */
  .menu-overlay {
    display: block !important; /* 強制顯示 */
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0s linear 0.3s;
  }

  /* 當菜單打開時顯示遮罩 */
  .nav-open + .menu-overlay {
    opacity: 1;
    visibility: visible;
    transition: opacity 0.3s ease, visibility 0s linear;
  }

  /* 導航菜單變為下拉式 */
  .nav {
    position: fixed;
    top: 0;
    right: -250px; /* 從右側滑入 */
    background-color: #f8f9fa;
    width: 250px;
    height: 100%;
    overflow-y: auto;
    transition: right 0.3s ease;
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
    padding-top: 60px; /* 為頂部預留空間 */
    z-index: 1000;
  }

  /* 當菜單打開時 */
  .nav.nav-open {
    right: 0;
  }

  /* 垂直排列導航項目 */
  .nav ul {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.5rem;
    width: 100%;
    box-sizing: border-box;
  }

  .nav li {
    width: 100%;
    margin: 5px 0;
    border-bottom: 1px solid #eee;
  }

  .nav li:last-child {
    border-bottom: none;
  }

  .nav a {
    padding: 15px;
    width: 100%;
    box-sizing: border-box;
    font-size: 18px;
    border-radius: 4px;
  }

  .nav a:hover,
  .nav a.router-link-active {
    background-color: rgba(0, 123, 255, 0.1);
  }

  .nav a::before {
    font-size: 1.3em;
    margin-right: 12px;
  }
}

/* 中型平板的調整 */
@media (max-width: 600px) {
  .header {
    padding: 10px 15px;
  }

  .logo {
    font-size: 18px;
  }
}

/* 小型手機的額外調整 */
@media (max-width: 480px) {
  .header {
    padding: 8px 12px;
  }

  .logo {
    font-size: 16px;
    max-width: calc(100% - 45px);
  }

  .nav {
    width: 220px;
  }

  .nav a {
    padding: 12px 15px;
    font-size: 16px;
  }
  .hamburger-icon {
    width: 24px;
    height: 24px;
  }
}
</style>
