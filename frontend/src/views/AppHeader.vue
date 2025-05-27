<template>
  <header class="header">
    <div class="logo">法國歷史全覽圖</div>
    <nav class="nav">
      <ul>
        <li><a href="/homepage">首頁</a></li>
        <li><a href="/mindmap">心智圖</a></li>
        <li><a href="/quizpage">小測驗</a></li>
      </ul>
    </nav>
  </header>
</template>

<style scoped>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* 讓 logo 靠左，nav 靠右 */
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-right: 30px;
}

.nav ul {
  list-style: none;
  margin: 0;
  padding: 0 1rem;
  display: flex;
  align-items: center;
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
}

.nav a.active {
  color: #007bff;
}

.nav a:hover {
  color: #007bff;
}

/* 添加圖標樣式 */
.nav a::before {
  display: inline-block;
  width: 1em;
  margin-right: 5px;
  font-size: 1em;
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
</style>
