from django import forms


class PostAddForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'file-upload'}
        ),
        label='',
    )
    content = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        ),
        label='',
    )


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
