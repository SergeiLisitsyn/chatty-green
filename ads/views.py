from posts.models import Post
from ads.models import Advertisement
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import AdvertisementForm


def home(request):
    latest_posts = Post.objects.filter(is_archived=False).order_by('-created_at')[:12]
    ads = Advertisement.objects.filter(is_active=True).order_by('-created_at')[:6]

    for ad in ads:
        if ad.image and ad.image.url.lower().endswith(('.mp4', '.webm')):
            ad.is_video = True
        else:
            ad.is_video = False

    return render(request, 'home.html', {
        'latest_posts': latest_posts,
        'ads': ads
    })



def advertisement_list(request):
    ads = Advertisement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'ads/ads_list.html', {'ads': ads})


@staff_member_required  # ✅ Только для админов
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ads:list')  # возвращаемся к списку объявлений
    else:
        form = AdvertisementForm()

    return render(request, 'ads/advertisement_form.html', {'form': form})
    pass