from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from member.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('age',)


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            if field == 'password1':
                pword = '비밀번호'
            else:
                pword = pword + ' 확인'
            self.fields[field].widget.attrs.update(
                {
                    'class': 'signup-field',
                    'placeholder': f'{pword}',
                }
            )
            self.fields['age'].required = False

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('nickname', 'img_profile', 'email', 'age',)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'signup-field',
                    'placeholder': '아이디',
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'signup-field',
                    'placeholder': '닉네임',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'signup-field',
                    'placeholder': '이메일',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'signup-field',
                    'placeholder': '나이',
                },
            ),
            'img_profile': forms.ClearableFileInput(
                attrs={
                    'class': 'signup-field',
                },
            )
        }

    def clean_username(self):
        cleaned_data = super().clean()
        if cleaned_data['username'][:3] == 'fb_':
            raise forms.ValidationError('유효하지 않은 아이디입니다.')
        else:
            return cleaned_data['username']


class LoginForm(forms.Form):
    """
    is_valiid() 에서 주어진 아이디/패스워드를 사용한 authenticate 실행,
    """
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        self.user = authenticate(
            username=username,
            password=password,
        )

        if not self.user:
            raise forms.ValidationError('아이디 또는 비밀번호가 잘못되었습니다.')
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        login(request, self.user)
