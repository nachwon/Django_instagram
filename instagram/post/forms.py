from django import forms

from post.models import Post


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'photo',
            'content',
        )
        widgets = {
            'photo': forms.ClearableFileInput(
                attrs={
                    'class': 'file-upload'
                },
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                },
            )
        }
        labels = {
            'photo': '',
            'content': '',
        }

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author is required')
            self.instance.author = author
        return super().save(*args, **kwargs)


class CommentAddForm(forms.Form):
    comment = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "comment-input-{{ post.pk }}",
                "class": "comment-input",
                "name": "comment",
                "type": "text",
                "placeholder": "댓글 달기...",
            }
        )
    )
