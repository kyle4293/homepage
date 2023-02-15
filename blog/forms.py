from django import forms
from .models import Post, Comment, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content']

        labels = {
            'subject': '제목',
            'content': '내용',
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Image
        fields = ['image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '답변',
        }

