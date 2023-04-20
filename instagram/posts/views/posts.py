# Python standard library
from typing import Any
from typing import Dict
from typing import Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
# Django views
from django.views import View
from django.views.generic.edit import FormMixin
# Django contrib and shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.posts.models import Post
# Instagram forms
from instagram.posts.forms import PostCreateForm


class PostCreateView(LoginRequiredMixin, FormMixin, View):
    
    form_class: Type[Form | ModelForm] = PostCreateForm
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
        
        return redirect('account:feed')