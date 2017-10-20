from django import forms

from post.models import Post


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'photo',
            'content',
        )

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author is required')
            self.instance.author = author
        return super().save(*args, **kwargs)

    # photo = forms.ImageField(
    #     widget=forms.FileInput(
    #         attrs={'class': 'file-upload'}
    #     ),
    #     label='',
    # )
    # content = forms.CharField(
    #     max_length=200,
    #     required=False,
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control'}
    #     ),
    #     label='',
    # )


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
