from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from social_django.models import UserSocialAuth
import urllib.parse
from unittest.mock import patch



class GoogleOAuthIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.ALLOWED_HOSTS.append('testserver')

    def setUp(self):
        self.client = Client()

    def test_complete_flow_with_mock(self):
        # 1. Start OAuth flow
        start_response = self.client.get(reverse('social:begin', args=['google-oauth2']))
        self.assertEqual(start_response.status_code, 302)

        # 2. Extract state from redirect URL
        redirect_url = start_response.url
        parsed = urllib.parse.urlparse(redirect_url)
        params = urllib.parse.parse_qs(parsed.query)
        state = params['state'][0]

        # 3. Mock callback from Google
        with self.settings(
            SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='test-key',
            SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='test-secret'
        ), patch('social_core.backends.google.GoogleOAuth2.get_json') as mock_get_json,  \
           patch('social_core.backends.google.GoogleOAuth2.request_access_token') as mock_token:

            # подставляем фейковые ответы
            mock_token.return_value = {'access_token': 'dummy-token'}
            mock_get_json.return_value = {
                'id': '123456789',
                'email': 'test@example.com',
                'name': 'Test User'
                 }

            response = self.client.get(
                reverse('social:complete', args=['google-oauth2']),
                {
                    'code': 'mock-code-123',
                    'state': state
                },
                follow=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(UserSocialAuth.objects.exists())


    
