from allauth.socialaccount.models import SocialApp
from django.conf import settings
from allauth.socialaccount import providers

def socialaccount_providers(request):
    available_providers = []
    # Перебираем все доступные провайдеры
    for provider in providers.registry.provider_map.values():
        # Фильтруем SocialApp по провайдеру и сайту
        if SocialApp.objects.filter(provider=provider.id, sites__id=settings.SITE_ID).exists():
            available_providers.append(provider)
    return {'socialaccount_providers': available_providers}
