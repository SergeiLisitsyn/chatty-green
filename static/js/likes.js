// Ожидаем полной загрузки DOM перед выполнением скрипта
document.addEventListener("DOMContentLoaded", function () {

  // ✅ БЛОК ЛАЙКОВ
  // Находим все кнопки с классом .like-button и вешаем обработчик клика
  document.querySelectorAll(".like-button").forEach(button => {
    button.addEventListener("click", async function () {
      const slug = this.dataset.slug;  // Получаем идентификатор поста (slug) из data-атрибута кнопки

      try {
        // Отправляем POST-запрос на лайк
        const response = await fetch(`/posts/${slug}/like/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),  // Передаём CSRF токен для Django
            "X-Requested-With": "XMLHttpRequest",  // Заголовок для распознавания AJAX-запроса
          },
        });

        // Получаем ответ от сервера и парсим его как JSON
        const data = await response.json();

        // Если сервер вернул успешный ответ
        if (data.success) {
          // Обновляем счётчик лайков на кнопке
          this.querySelector(".like-count").textContent = data.likes_count;

          // Переключаем состояние кнопки (например, выделение)
          this.classList.toggle("active");
        } else {
          console.error("❌ Ошибка: сервер не вернул статус success.");
        }
      } catch (error) {
        // В случае ошибки запроса выводим сообщение в консоль
        console.error("❌ Ошибка запроса лайка:", error);
      }
    });
  });

  // ✅ БЛОК ДИЗЛАЙКОВ
  // Аналогично блоку лайков, только для дизлайков
  document.querySelectorAll(".dislike-button").forEach(button => {
    button.addEventListener("click", async function () {
      const slug = this.dataset.slug;

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

  // ✅ БЛОК ПЕРЕХОДА К КОММЕНТАРИЯМ
  // При клике на кнопку комментариев переходим к блоку #comments соответствующего поста
  document.querySelectorAll(".comment-button").forEach(button => {
    button.addEventListener("click", function () {
      const slug = this.dataset.slug;
      window.location.href = `/posts/${slug}/#comments`;  // Прокрутка к блоку комментариев
    });
  });

  // ✅ БЛОК АРХИВИРОВАНИЯ И УДАЛЕНИЯ ПОСТА
  // При клике на кнопку архивации подтверждаем удаление и отправляем POST-запрос
  document.querySelectorAll(".archive-post").forEach(button => {
    button.addEventListener("click", async function () {
      const postId = this.dataset.id;

      // Подтверждение действия от пользователя
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

          // Удаляем HTML-элемент поста со страницы
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

// ✅ ФУНКЦИЯ ПОЛУЧЕНИЯ CSRF ТОКЕНА ИЗ COOKIE
function getCSRFToken() {
  let cookieValue = null;

  // Перебираем все cookie браузера
  document.cookie.split(";").forEach(cookie => {
    const trimmed = cookie.trim();

    // Ищем cookie, начинающееся с 'csrftoken='
    if (trimmed.startsWith("csrftoken=")) {
      cookieValue = decodeURIComponent(trimmed.split("=")[1]);
    }
  });

  return cookieValue;
}
