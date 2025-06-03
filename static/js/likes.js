//static/js/likes.js

// Ожидаем полной загрузки DOM перед выполнением скрипта
document.addEventListener("DOMContentLoaded", function () {

  /**
   * Функция обновления состояния кнопок лайка и дизлайка для конкретного поста (по slug)
   * Обновляет счетчики и активные классы кнопок.
   * @param {string} slug - уникальный идентификатор поста
   * @param {boolean} liked - поставлен ли лайк пользователем
   * @param {boolean} disliked - поставлен ли дизлайк пользователем
   * @param {number} likes_count - текущее количество лайков
   * @param {number} dislikes_count - текущее количество дизлайков
   */
  function updateButtons(slug, liked, disliked, likes_count, dislikes_count) {
    // Находим кнопку лайка по slug
    const likeBtn = document.querySelector(`.like-button[data-slug="${slug}"]`);
    // Находим кнопку дизлайка по slug
    const dislikeBtn = document.querySelector(`.dislike-button[data-slug="${slug}"]`);

    // Обновляем кнопку лайка, если она есть
    if (likeBtn) {
      // Обновляем количество лайков в кнопке
      likeBtn.querySelector(".like-count").textContent = likes_count;
      // Добавляем или убираем класс active в зависимости от состояния liked
      if (liked) likeBtn.classList.add("active");
      else likeBtn.classList.remove("active");
    }

    // Обновляем кнопку дизлайка, если она есть
    if (dislikeBtn) {
      // Обновляем количество дизлайков в кнопке
      dislikeBtn.querySelector(".dislike-count").textContent = dislikes_count;
      // Добавляем или убираем класс active в зависимости от состояния disliked
      if (disliked) dislikeBtn.classList.add("active");
      else dislikeBtn.classList.remove("active");
    }
  }

  // ✅ БЛОК ЛАЙКОВ
  // Находим все кнопки с классом .like-button и вешаем обработчик клика
  document.querySelectorAll(".like-button").forEach(button => {
    // Добавляем курсор указателя для интерактивности
    button.style.cursor = "pointer";

    button.addEventListener("click", async function () {
      // Получаем slug (уникальный идентификатор поста) из data-атрибута кнопки
      const slug = this.dataset.slug;
      // Тип контента, если не указан, по умолчанию "posts"
      const type = this.dataset.type || "posts";

      try {
        // Отправляем POST-запрос на сервер для лайка
        const response = await fetch(`/${type}/${slug}/like/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),  // Передаем CSRF токен для защиты
            "X-Requested-With": "XMLHttpRequest",  // Заголовок для распознавания AJAX-запроса на сервере
          },
        });

        // Парсим ответ сервера как JSON
        const data = await response.json();

        // Если сервер вернул успешный ответ
        if (data.success) {
          // Обновляем кнопки лайка и дизлайка на странице с учетом данных с сервера
          updateButtons(slug, data.liked, false, data.likes_count, data.dislikes_count);
        } else {
          // Если успеха нет, выводим ошибку в консоль
          console.error("❌ Ошибка: сервер не вернул статус success.");
        }
      } catch (error) {
        // При ошибке запроса выводим ошибку в консоль
        console.error("❌ Ошибка запроса лайка:", error);
      }
    });
  });

  // ✅ БЛОК ДИЗЛАЙКОВ
  // Аналогично блоку лайков, но для дизлайков
  document.querySelectorAll(".dislike-button").forEach(button => {
    button.style.cursor = "pointer"; // Добавляем курсор для интерактивности

    button.addEventListener("click", async function () {
      const slug = this.dataset.slug;
      const type = this.dataset.type || "posts";

      try {
        // Отправляем POST-запрос на дизлайк
        const response = await fetch(`/${type}/${slug}/dislike/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.success) {
          // Обновляем кнопки лайка и дизлайка с учетом ответа сервера
          updateButtons(slug, false, data.disliked, data.likes_count, data.dislikes_count);
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
      // Переходим по адресу поста с якорем на комментарии
      window.location.href = `/posts/${slug}/#comments`;
    });
  });

  // ✅ БЛОК АРХИВИРОВАНИЯ И УДАЛЕНИЯ ПОСТА
  // При клике на кнопку архивации подтверждаем удаление и отправляем POST-запрос
  document.querySelectorAll(".archive-post").forEach(button => {
    button.addEventListener("click", async function () {
      const postId = this.dataset.id;

      // Запрашиваем подтверждение действия у пользователя
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
          // Удаляем HTML-элемент поста со страницы по id
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

/**
 * ФУНКЦИЯ ПОЛУЧЕНИЯ CSRF ТОКЕНА ИЗ COOKIE
 * Возвращает значение токена csrftoken, если он есть в cookie браузера
 */
function getCSRFToken() {
  let cookieValue = null;

  // Перебираем все cookie браузера
  document.cookie.split(";").forEach(cookie => {
    const trimmed = cookie.trim();

    // Ищем cookie, начинающееся с 'csrftoken='
    if (trimmed.startsWith("csrftoken=")) {
      // Извлекаем значение токена из cookie
      cookieValue = decodeURIComponent(trimmed.split("=")[1]);
    }
  });

  return cookieValue;
}
