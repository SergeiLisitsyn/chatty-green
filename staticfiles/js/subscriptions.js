function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Subscription script loaded!');

    const subscriptionButtons = document.querySelectorAll('.subscription-toggle, [data-username], .otpis-btn');
    console.log('Found subscription elements:', subscriptionButtons.length);

    document.addEventListener('click', function(event) {
        if (event.target.closest('[data-username], .subscription-toggle, .otpis-btn') ||
            event.target.textContent.includes('Отписаться')) {

            const button = event.target.closest('button, [type="submit"]');
            if (!button) return;

            event.preventDefault();
            console.log('Subscription button clicked:', button);

            let username = button.dataset.username;
            if (!username && button.form) {
                const formAction = button.form.action;
                const matches = formAction.match(/\/subscriptions\/toggle\/([^\/]+)\//);
                if (matches && matches[1]) {
                    username = matches[1];
                }
            }

            if (!username) {
                const parentWithUsername = button.closest('[data-username]');
                if (parentWithUsername) {
                    username = parentWithUsername.dataset.username;
                }
            }

            if (!username) {
                console.error('Could not determine username for subscription toggle');
                return;
            }

            console.log('Processing subscription for username:', username);

            const originalHTML = button.innerHTML;
            const originalDisabled = button.disabled;

            button.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i>';
            button.disabled = true;

            const csrftoken = getCookie('csrftoken');
            console.log('CSRF Token:', csrftoken);

            const controller = new AbortController();
            const signal = controller.signal;

            const fetchTimeout = setTimeout(() => {
                controller.abort();
                console.error('Запрос прерван из-за таймаута');
                alert('Сервер не отвечает, попробуйте позже.');
                button.innerHTML = originalHTML;
                button.disabled = originalDisabled;
            }, 5000); // Таймаут запроса 5 секунд

            fetch('http://host.docker.internal:8000/subscriptions/toggle/' + username, {

                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                credentials: 'same-origin',
                signal
            })
            .then(response => {
                clearTimeout(fetchTimeout); // Сбрасываем таймаут при успешном ответе

                if (!response.ok) {
                    throw new Error(`Ошибка сервера: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Server response:', data);

                const subscribersCountElem = document.getElementById('subscribers-count');
                if (subscribersCountElem) {
                    subscribersCountElem.textContent = data.subscribers_count;
                }

                if (data.is_subscribed) {
                    button.innerHTML = '<i class="fa-solid fa-user-minus me-1 text-warning"></i> Отписаться';
                } else {
                    button.innerHTML = '<i class="fa-solid fa-user-plus me-1 text-warning"></i> Подписаться';
                }
                button.disabled = false;
            })
            .catch(error => {
                console.error('Ошибка подписки:', error);
                button.innerHTML = originalHTML;
                button.disabled = originalDisabled;
                alert('Произошла ошибка при обработке запроса: ' + error.message);
            });
        }
    });
});
