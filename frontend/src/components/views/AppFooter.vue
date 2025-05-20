<template>
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h3 class="footer-title">關於我們</h3>
                    <p>我們致力於提供智能工具，幫助用戶探索法國歷史，通過心智圖和測驗提升學習效率。</p>
                </div>
                <div class="footer-col">
                    <h3 class="footer-title">快速連結</h3>
                    <ul class="footer-list">
                        <li><a href="/homepage">首頁</a></li>
                        <li><a href="/mindmap">心智圖</a></li>
                        <li><a href="/quizpage">小測驗</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3 class="footer-title">聯繫資訊</h3>
                    <ul class="footer-list">
                        <li>Email: <a href="mailto:support@example.com">support@example.com</a></li>
                        <li>電話: +886 123 456 789</li>
                        <li>地址: 台北市中正區歷史路 123 號</li>
                    </ul>
                </div>
            </div>
            <div class="footer-copyright">
                <p>©2025 Spring - AI project</p>
            </div>
        </div>
    </footer>
</template>

<style scoped>
.footer {
    background-color: #F3F4F6;
    color: #4B5563;
    padding: 2rem 3rem;
    margin-top: 2rem;
}

.footer-container {
    max-width: 1024px;
    margin: 0 auto;
}

.footer-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
}

@media (min-width: 768px) {
    .footer-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

.footer-col {
    padding: 0 1rem;
    text-align: left;
}

.footer-title {
    font-size: 1.125rem;
    font-weight: bold;
    color: #2563EB;
    margin-bottom: 1rem;
}

.footer-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-list li {
    margin-bottom: 0.5rem;
}

.footer-list a {
    color: #2563EB;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-list a:hover {
    color: #1E40AF;
}

.footer-grid p,
.footer-col p {
    font-size: 0.875rem;
    line-height: 1.6;
}

.footer-grid li {
    font-size: 0.875rem;
    line-height: 1.6;
}

.footer-grid a {
    font-size: 0.875rem;
}

.footer-copyright {
    border-top: 1px solid #D1D5DB;
    margin-top: 2rem;
    padding-top: 1rem;
    text-align: left;
}

.footer-copyright p {
    font-size: 0.75rem;
    color: #6B7280;
}
</style>
