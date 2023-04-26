from django import forms


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


class EmptyForm(forms.Form):
    pass