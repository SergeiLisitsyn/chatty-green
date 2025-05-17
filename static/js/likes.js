document.addEventListener("DOMContentLoaded", function () {
  // ✅ Лайк поста
  document.querySelectorAll(".like-button").forEach(button => {
    button.addEventListener("click", async function () {
      const slug = this.dataset.slug;  // ✅ ИСПРАВЛЕНО: использовано правильное имя переменной

      try {
        const response = await fetch(`/posts/${slug}/like/`, {  // ✅ Используем переменную slug
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();
        if (data.success) {
          this.querySelector(".like-count").textContent = data.likes_count;
          this.classList.toggle("active");
        } else {
          console.error("❌ Ошибка: сервер не вернул статус success.");
        }
      } catch (error) {
        console.error("❌ Ошибка запроса лайка:", error);
      }
    });
  });

  // ✅ Дизлайк поста
  document.querySelectorAll(".dislike-button").forEach(button => {
    button.addEventListener("click", async function () {
      const slug = this.dataset.slug;  // ✅ Оставляем `slug`

      try {
        const response = await fetch(`/posts/${slug}/dislike/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();
        if (data.success) {
          this.querySelector(".dislike-count").textContent = data.dislikes_count;
          this.classList.toggle("active");
        } else {
          console.error("❌ Ошибка: сервер не вернул статус success.");
        }
      } catch (error) {
        console.error("❌ Ошибка запроса дизлайка:", error);
      }
    });
  });

  // ✅ Комментарии - переход к блоку комментариев
  document.querySelectorAll(".comment-button").forEach(button => {
    button.addEventListener("click", function () {
      const slug = this.dataset.slug;
      window.location.href = `/posts/${slug}/#comments`;
    });
  });

  // ✅ Автоматическое удаление поста после архивирования
  document.querySelectorAll(".archive-post").forEach(button => {
    button.addEventListener("click", async function () {
      const postId = this.dataset.id;

      if (!confirm("Вы уверены, что хотите заархивировать и удалить этот пост?")) return;

      try {
        const response = await fetch(`/posts/${postId}/archive/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.success) {
          alert("✅ Пост успешно архивирован и удалён!");
          document.getElementById(`post-${data.post_id}`).remove();
        } else {
          alert("❌ Ошибка при архивировании!");
        }
      } catch (error) {
        console.error("❌ Ошибка архивирования:", error);
        alert("❌ Ошибка архивирования поста.");
      }
    });
  });
});

// ✅ Функция получения CSRF-токена
function getCSRFToken() {
  let cookieValue = null;
  document.cookie.split(";").forEach(cookie => {
    const trimmed = cookie.trim();
    if (trimmed.startsWith("csrftoken=")) {
      cookieValue = decodeURIComponent(trimmed.split("=")[1]);
    }
  });
  return cookieValue;
}
