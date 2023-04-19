from django import forms


class PostCreateForm(forms.Form):
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={ 'id': 'image_upload' })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={ 'id': 'description', 'placeholder': 'Write a description here' }
        )
    )