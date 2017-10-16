from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'signup-field',
                'placeholder': '아이디',
            }
        ),
        label='',
    )
    mail = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'signup-field',
                'placeholder': '이메일',
            }
        ),
        label='',
        required=False,
    )
    password_1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup-field password',
                'placeholder': '비밀번호',
            }
        ),
        label='',
    )
    password_2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup-field password',
                'placeholder': '비밀번호 확인',
            }
        ),
        label='',
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'signup-field',
                'placeholder': '아이디',
            }
        ),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup-field password',
                'placeholder': '비밀번호',
            }
        ),
        label='',
    )
