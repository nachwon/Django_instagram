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

