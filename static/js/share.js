//static/js/share.js
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-share").forEach(button => {
    button.addEventListener("click", async function () {
      const postUrl = this.dataset.url;

      try {
        await navigator.clipboard.writeText(postUrl);
        alert("📋 Ссылка на пост скопирована в буфер обмена!");
      } catch (err) {
        console.error("❌ Ошибка копирования ссылки:", err);
        alert("❌ Не удалось скопировать ссылку. Попробуйте вручную.");
      }
    });
  });
});
