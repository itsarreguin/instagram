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
from django.views.generic import ListView
# Django database
from django.db.models import Model
from django.db.models import QuerySet
# Django forms
from django.forms import BaseForm
# Django contrib and shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
# Django urls
from django.urls import reverse
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
from instagram.posts.models import Post
from instagram.posts.models import Collection
# Instagram forms
from instagram.posts.forms import NewCollectionForm


class CollectionsView(LoginRequiredMixin, ListView):

    model: Type[Model] = Collection
    template_name: str = 'bookmarks.html'

    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return self.model.objects.filter(*args, **kwargs).all()

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['collections'] = self.get_queryset(user=self.request.user)
        context['form'] = NewCollectionForm

        return context


class NewCollectionView(LoginRequiredMixin, FormMixin, View):

    form_class: Type[BaseForm] = NewCollectionForm

    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            Collection.objects.create(
                user=request.user,
                name=form.cleaned_data['name']
            )
            return redirect('account:bookmarks', username=request.user.username)

        return HttpResponseRedirect(reverse('account:feed'))


class CollectionDetailView(LoginRequiredMixin, ContextMixin, View):

    model: Type[Model] = Collection
    template_name: str = 'collection.html'

    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        queryset = (
            self.model.objects.filter(*args, **kwargs)
            .prefetch_related('posts', 'posts__comments', 'posts__likes').first()
        )
        return queryset

    def get_object(self) -> Type[User]:
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['collection'] = (
            self.get_queryset(user=self.get_object(), slug=kwargs['slug'])
        )

        return context

    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class SaveToCollectionView(LoginRequiredMixin, View):

    template_name: str = 'includes/save.html'

    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        user = User.objects.filter(username=kwargs['username']).first()
        post_to_save = Post.objects.filter(url=kwargs['post_url']).first()
        collection = (
            Collection.objects
            .filter(user=user, slug=kwargs['coll_slug']).first()
        )
        if not post_to_save in collection.posts.all():
            collection.posts.add(post_to_save)
        else:
            collection.posts.remove(post_to_save)

        context = {
            'post': post_to_save,
            'collection': collection
        }
        return render(request, self.template_name, context)