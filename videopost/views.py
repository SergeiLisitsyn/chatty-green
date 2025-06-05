# videopost/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from .models import VideoPost, VideoComment
from .forms import VideoCommentForm, VideoPostForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from subscriptions.models import Subscription
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.http import require_GET
# from .models import Subscription
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

class VideoPostCreateView(LoginRequiredMixin, CreateView):
    model = VideoPost
    form_class = VideoPostForm
    template_name = 'videopost/videopost_form.html'
    success_url = reverse_lazy('videopost:videopost_list')

    def form_valid(self, form):
        # Присваиваем текущего пользователя как автора видеопоста
        form.instance.author = self.request.user
        return super().form_valid(form)


class VideoPostListView(ListView):
    model = VideoPost
    template_name = 'videopost/videopost_list.html'  # Исправлено название шаблона для единообразия
    context_object_name = 'videopost'
    paginate_by = 5

    def get_queryset(self):
        return VideoPost.objects.filter(is_archived=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get("paginator")
        page = self.request.GET.get("page")

        try:
            page = int(page) if page else 1
            if page > paginator.num_pages:
                context["invalid_page"] = True
                context["last_page"] = paginator.num_pages
        except (ValueError, PageNotAnInteger, EmptyPage):
            context["invalid_page"] = True
            context["last_page"] = 1

        # --- ДОПОЛНЕНИЕ ---
        # Добавляем текущего пользователя в контекст для удобства в шаблоне
        context['current_user'] = self.request.user

        return context


class VideoPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoPost
    form_class = VideoPostForm
    template_name = 'videopost/videopost_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('videopost:videopost_detail', kwargs={'slug': self.object.slug})


class VideoPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoPost
    success_url = reverse_lazy('videopost:videopost_list')
    template_name = 'videopost/video_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class VideoPostDetailView(DetailView):
    model = VideoPost
    template_name = 'videopost/videopost_detail.html'
    context_object_name = 'videopost'

    def get_queryset(self):
        # Показываем только неархивированные видео
        return VideoPost.objects.filter(is_archived=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videopost = self.get_object()
        context['comments'] = self.object.comments.filter(parent__isnull=True)
        context['form'] = VideoCommentForm()
               # --- ДОБАВЛЯЕМ is_subscribed ---
        user = self.request.user
        if user.is_authenticated and user != videopost.author:
            from subscriptions.models import Subscription
            context['is_subscribed'] = Subscription.objects.filter(
                subscriber=user, author=videopost.author
            ).exists()
        else:
            context['is_subscribed'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = VideoCommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('videopost:videopost_detail', slug=self.object.slug)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


@login_required
@require_POST
def toggle_videolike(request, slug):
    video = get_object_or_404(VideoPost, slug=slug)
    user = request.user

    if video.likes.filter(id=user.id).exists():
        # Пользователь уже лайкнул — снимаем лайк
        video.likes.remove(user)
        liked = False
    else:
        # Снимаем дизлайк, если есть
        if video.dislikes.filter(id=user.id).exists():
            video.dislikes.remove(user)
        # Добавляем лайк
        video.likes.add(user)
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': video.likes.count(),
        'dislikes_count': video.dislikes.count(),
    })

@login_required
@require_POST
def toggle_videodislike(request, slug):
    video = get_object_or_404(VideoPost, slug=slug)
    user = request.user

    if video.dislikes.filter(id=user.id).exists():
        # Пользователь уже дизлайкнул — снимаем дизлайк
        video.dislikes.remove(user)
        disliked = False
    else:
        # Снимаем лайк, если есть
        if video.likes.filter(id=user.id).exists():
            video.likes.remove(user)
        # Добавляем дизлайк
        video.dislikes.add(user)
        disliked = True

    return JsonResponse({
        'success': True,
        'disliked': disliked,
        'likes_count': video.likes.count(),
        'dislikes_count': video.dislikes.count(),
    })


class VideoPostDetailViewId(DetailView):
    model = VideoPost
    template_name = 'videopost/videopost_detail.html'
    context_object_name = 'videopost'
    pk_url_kwarg = 'pk'


class VideoFeedView(LoginRequiredMixin, ListView):
    model = VideoPost
    template_name = 'videopost/feed.html'
    context_object_name = 'videopost'
    paginate_by = 10

    def get_queryset(self):
        subscribed_authors = Subscription.objects.filter(subscriber=self.request.user).values_list('author', flat=True)
        return VideoPost.objects.filter(author__in=subscribed_authors).order_by('-publication_date')


def archive_videopost(request, slug):
    if request.method == "POST":
        post = get_object_or_404(VideoPost, slug=slug)
        if request.user == post.author:
            post.is_archived = True
            post.save()
            return JsonResponse({'success': True})
        else:
            return HttpResponseForbidden("Вы не являетесь автором этого поста.")
    else:
        return HttpResponseForbidden("Недопустимый метод запроса.")


def delete_videopost(request, slug):
    if request.method == "POST":
        post = get_object_or_404(VideoPost, slug=slug)
        if request.user == post.author:
            post.is_archived = True
            post.save()
            return JsonResponse({"success": True, "post_id": post.id, "message": "✅ Ваш видеопост успешно удалён!"})
        else:
            return HttpResponseForbidden("Вы не являетесь автором этого поста.")
    else:
        return HttpResponseForbidden("Недопустимый метод запроса.")


def search_video_results(request):
    query = request.GET.get("q", "").strip()
    videopost = VideoPost.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_archived=False
    )

    # --- ДОПОЛНЕНИЕ ---
    # Добавлена пагинация для результатов поиска
    paginator = Paginator(videopost, 10)  # 10 на страницу
    page = request.GET.get('page')

    try:
        videopost_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        videopost_page = paginator.page(1)

    return render(request, "videopost/search_results.html", {
        "videopost": videopost_page,
        "query": query
    })


@require_GET
def videopost_api_detail(request, slug):
    post = get_object_or_404(VideoPost, slug=slug)
    data = {
        "id": post.id,
        "title": post.title,
        "description": post.description,
        "author": post.author.username,
        "likes_count": post.likes.count(),
        "dislikes_count": post.dislikes.count(),
        "created_at": post.created_at.isoformat(),
            }
    return JsonResponse(data)

def add_comment(request, slug):
    videopost = get_object_or_404(VideoPost, slug=slug)

    if request.method == "POST":
        text = request.POST.get("text")
        parent_id = request.POST.get("parent_id", None)

        # Проверяем, что текст не пустой
        if not text.strip():
            return JsonResponse({"error": "Комментарий не может быть пустым"}, status=400)

        # Создание комментария с правильной привязкой
        comment = VideoComment.objects.create(
            post=videopost,  # ✅ Исправлено: у модели VideoComment поле называется post, а не videopost
            author=request.user,
            text=text.strip(),
            parent_id=VideoComment.objects.filter(id=parent_id).first() if parent_id else None
        )

        return redirect(videopost.get_absolute_url())

    return JsonResponse({"error": "Метод запроса должен быть POST"}, status=405)

@login_required
@require_POST
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(VideoComment, id=comment_id)
    text = request.POST.get("text")

    if not text.strip():
        return JsonResponse({"error": "Комментарий не может быть пустым"}, status=400)

    reply = VideoComment.objects.create(
        post=parent_comment.post,  # Привязываем к тому же `VideoPost`
        author=request.user,
        text=text.strip(),
        parent=parent_comment
    )

    return redirect(parent_comment.post.get_absolute_url())

@require_POST
@login_required
def share_videopost(request):
    try:
        data = json.loads(request.body)
        platform = data.get('platform')
        recipient = data.get('recipient')
        url = data.get('url')

        if platform != 'email':
            return JsonResponse({'status': 'error', 'message': 'Поддерживается только email'}, status=400)

        if not recipient or not url:
            return JsonResponse({'status': 'error', 'message': 'Не указан email или ссылка'}, status=400)

        subject = "Смотрите интересный пост!"
        message = (
            f"Пользователь {request.user.username} ({request.user.email}) "
            f"поделился с вами ссылкой на пост:\n\n{url}"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
        )

        return JsonResponse({'status': 'success', 'message': 'Письмо отправлено!'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

