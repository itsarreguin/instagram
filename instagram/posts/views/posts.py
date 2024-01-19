# Python standard library
from typing import Any, Dict, Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import View
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
# Django DB
from django.db.models import QuerySet
from django.db.models import Prefetch
# Django contrib and shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
# Django urls
from django.urls import reverse
# Django forms
from django.forms import BaseForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.posts.models import Post
from instagram.posts.models import Like
from instagram.posts.models import Comment
from instagram.notifications.models import NotificationType
# Instagram forms
from instagram.posts.forms import PostCreateForm
from instagram.posts.forms import CommentForm
# Instagram tasks
from instagram.notifications.tasks import send_notification


class PostCreateView(LoginRequiredMixin, FormMixin, View):

    form_class: Type[BaseForm] = PostCreateForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                author=request.user,
                image=form.cleaned_data['image'],
                thumbnail=form.cleaned_data['image'],
                description=form.cleaned_data['description']
            )
            return redirect(request.META['HTTP_REFERER'])

        return HttpResponseRedirect(reverse('account:feed'))


class PostDetailView(LoginRequiredMixin, ContextMixin, View):

    template_name: str = 'post_detail.html'

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Post]:
        return Post.objects.filter(*args, **kwargs)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        comments = Prefetch(
            lookup='comments',
            queryset=(
                Comment.objects.filter(post__url=kwargs['url'])
                .select_related('author', 'author__profile', 'post')
                .order_by('-created').all()
            )
        )
        context['post'] = (
            self.get_queryset(url=kwargs['url']).select_related('author', 'author__profile')
            .prefetch_related(comments, 'likes').first()
        )
        context['comment_form'] = CommentForm

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class PostDeleteView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = Post.objects.filter(**{ 'url': kwargs['url'] }).first()

        if query is not None and query.author == request.user:
            query.delete()
            return HttpResponseRedirect(reverse('account:feed'))

        return HttpResponseRedirect(reverse('account:feed'))


class LikeView(LoginRequiredMixin, FormMixin, View):

    model: Type[Like] = Like
    template_name: str = 'includes/like.html'

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Like]:
        return self.model.objects.filter(*args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post = Post.objects.get(url=kwargs['url'])
        like = self.get_queryset(user=request.user, post=post).first()

        if like is not None:
            like.delete()
        else:
            like = self.model.objects.create(user=request.user, post=post)
            if request.user != post.author:
                send_notification.apply_async(kwargs={
                    'receiver_username': post.author.username,
                    'sender_username': request.user.username,
                    'category': NotificationType.LIKE,
                    'object_id': post.id,
                    'object_slug': post.url
                })

        return render(request, self.template_name, { 'post': post, 'like': like })


class CommentView(LoginRequiredMixin, ContextMixin, View):

    form_class: Type[BaseForm] = CommentForm
    model: Type[Comment] = Comment

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Post]:
        return Post.objects.filter(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_queryset(url=kwargs['url']).first()
        context['comment_form'] = self.form_class

        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST or None)
        post = self.get_queryset(**{ 'url': kwargs['url'] }).first()

        if form.is_valid():
            self.model.objects.create(
                author=request.user,
                post=post,
                body=form.cleaned_data['body']
            )
            if request.user != post.author:
                send_notification.apply_async(kwargs={
                    'receiver_username': post.author.username,
                    'sender_username': request.user.username,
                    'category': NotificationType.COMMENT,
                    'object_id': post.id,
                    'object_slug': post.url
                })

        return render(request, self.template_name, self.get_context_data(**kwargs))


class CommentFeedView(CommentView):
    template_name: str = 'includes/comments-counter.html'


class CommentCreateView(CommentView):
    template_name: str = 'includes/post_card_detail.html'