from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from social_core.backends.google import GoogleOAuth2
from social_django.utils import load_strategy
from unittest.mock import patch
from django.urls import reverse
from django.conf import settings
import json

class GoogleOAuthUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'test-key'
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'test-secret'
        settings.SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['state']

    def test_backend_auth_complete(self):
        # 1. Создаем запрос с параметрами
        request = self.factory.get(
            reverse('social:complete', args=['google-oauth2']),
            {
                'code': 'mock-code-123',
                'state': 'test-state-123'
            }
        )
        
        # 2. Настраиваем сессию правильно
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        
        # 3. Сохраняем state в сессию в том формате, который ожидает social auth
        request.session['social_auth_state'] = json.dumps({
            'google-oauth2': {
                'state': 'test-state-123',
                'data': {}
            }
        })
        request.session.save()
        
        # 4. Создаем стратегию и бэкенд
        strategy = load_strategy(request=request)
        backend = GoogleOAuth2(strategy=strategy)
        
        # 5. Настраиваем моки
        with patch('social_core.backends.google.GoogleOAuth2.get_json') as mock_get_json, \
             patch('social_core.backends.oauth.BaseOAuth2.request_access_token') as mock_token:
            
            mock_token.return_value = {
                'access_token': 'test-token',
                'token_type': 'Bearer',
                'expires_in': 3600
            }
            
            mock_get_json.return_value = {
                'email': 'test@example.com',
                'given_name': 'Test',
                'family_name': 'User',
                'sub': '1234567890'
            }
            
            # 6. Выполняем аутентификацию
            user = backend.auth_complete()
            
            # 7. Проверяем результат
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')
