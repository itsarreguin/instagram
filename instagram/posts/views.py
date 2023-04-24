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
# Django contrib and shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.posts.models import Post
from instagram.posts.models import Like
from instagram.posts.models import Comment
# Instagram forms
from instagram.posts.forms import PostCreateForm
from instagram.posts.forms import EmptyForm


class PostCreateView(LoginRequiredMixin, FormMixin, View):
    
    form_class: Type[Form | ModelForm] = PostCreateForm
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                author=request.user,
                image=form.cleaned_data['image'],
                thumbnail=form.cleaned_data['image'],
                description=form.cleaned_data['description']
            )
            return redirect('account:feed')
        
        return redirect('account:feed')


class PostDetailView(LoginRequiredMixin, ContextMixin, View):
    
    template_name: str = 'post_detail.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Post.objects.filter(*args, **kwargs)
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_queryset(url=self.kwargs['url']).first()
        context['comments'] = Comment.objects.all()
        
        return context
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class LikeView(LoginRequiredMixin, View):
    
    form_class: Type[Form | ModelForm] = EmptyForm
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return Like.objects.filter(*args, **kwargs).first()
        return Like.objects.all()
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        post = Post.objects.filter(**{ 'url': kwargs['url'] }).first()
        like = self.get_queryset(user=request.user, post=post)
        
        if like is not None:
            like.delete()
            return redirect('account:feed')
        if form.is_valid():
            Like.objects.create(user=request.user, post=post)
            return redirect('account:feed')
        
        return redirect('account:feed')