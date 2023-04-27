# Python standard library
from typing import Dict
from typing import List
from typing import Type

# Django imports
from django import forms
from django.db.models import Model

# Instagram models
from instagram.posts.models import Collection


class PostCreateForm(forms.Form):
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={ 'id': 'post-image' })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={ 'id': 'description', 'placeholder': 'Write a description here' }
        )
    )


class CommentForm(forms.Form):
    
    body = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'body',
                'class': 'input-comment', 'placeholder': 'Add a comment ...'
            }
        )
    )


class NewCollectionForm(forms.ModelForm):
    
    class Meta:
        model: Type[Model] = Collection
        fields: List[str] = ['name']
        widgets: Dict[str, object] = {
            'name': forms.TextInput(
                attrs={ 'class': 'input-auth', 'placeholder': 'Name for your new collection'}
            )
        }


class EmptyForm(forms.Form):
    pass