# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type

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
from django.db.models import Model
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
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
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
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Post.objects.filter(*args, **kwargs)
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_queryset(url=self.kwargs['url']).first()
        context['comments'] = (
            Comment.objects
            .filter(post__url=self.kwargs['url'])
            .order_by('-created')
            .all()
        )
        context['comment_form'] = CommentForm
        
        return context
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class LikeView(LoginRequiredMixin, FormMixin, View):
    
    template_name: str = 'includes/like.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Like.objects.filter(*args, **kwargs)
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        post = Post.objects.filter(url=kwargs['url']).first()
        like = self.get_queryset(user=request.user, post=post).first()
        if like:
            like.delete()
        else:
            like = Like.objects.create(user=request.user, post=post)
            if request.user != post.author:
                send_notification.apply_async(kwargs={
                    'receiver_username': post.author.username,
                    'sender_username': request.user.username,
                    'category': NotificationType.LIKE,
                    'object_id': post.id,
                    'object_slug': post.url
                })

        context = {
            'post': post,
            'like': like
        }
        return render(request, self.template_name, context)


class CommentFeedView(LoginRequiredMixin, ContextMixin, View):
    
    template_name: str = 'includes/comments-counter.html'
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = CommentForm(request.POST or None)
        post = Post.objects.filter(url=kwargs['url']).first()
        if form.is_valid():
            Comment.objects.create(
                author=self.request.user,
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
        
        return render(request, self.template_name, { 'post': post })
            

class CommentCreateView(LoginRequiredMixin, ContextMixin, View):
    
    form_class: Type[BaseForm] = CommentForm
    template_name: str = 'includes/post_card_detail.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Post.objects.filter(*args, **kwargs).first()
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_queryset(url=self.kwargs['url'])
        context['comments'] = (
            Comment.objects
            .filter(post__url=self.kwargs['url'])
            .order_by('-created').all()
        )
        context['comment_form'] = self.form_class
        
        return context
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        post = Post.objects.filter(url=kwargs['url']).first()
        if form.is_valid():
            Comment.objects.create(
                author=self.request.user,
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
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)