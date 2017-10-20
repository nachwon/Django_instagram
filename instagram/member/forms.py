from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from member.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('age',)


# class SignUpForm(forms.Form):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'signup-field',
    #             'placeholder': '아이디',
    #         }
    #     ),
    #     label='',
    # )
    # mail = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             'class': 'signup-field',
    #             'placeholder': '이메일',
    #         }
    #     ),
    #     label='',
    #     required=False,
    # )
    # password_1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'signup-field password',
    #             'placeholder': '비밀번호',
    #         }
    #     ),
    #     label='',
    # )
    # password_2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'signup-field password',
    #             'placeholder': '비밀번호 확인',
    #         }
    #     ),
    #     label='',
    # )
    #
    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     user_exists = User.objects.filter(username=data).exists()
    #     if user_exists:
    #         raise forms.ValidationError('유저가 이미 존재합니다.')
    #     return data
    #
    # def clean_password_2(self):
    #     data = self.cleaned_data['password_2']
    #     if self.cleaned_data['password_1'] != data:
    #         raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
    #     return data
    #
    # def clean(self):
    #     if self.is_valid():
    #         setattr(self, 'signup', self._signup)
    #     return self.cleaned_data
    #
    # def _signup(self):
    #     username = self.cleaned_data.get('username')
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password_2')
    #     return User.objects.create_user(username=username, email=email, password=password)


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            if field == 'password1':
                pword = '비밀번호'
            else:
                pword = '비밀번호 확인'
            self.fields[field].widget.attrs.update(
                {
                    'class': 'signup-field',
                    'placeholder': f'{pword}',
                }
            )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('img_profile', 'email', 'age',)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'signup-field',
                    'placeholder': '아이디',
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
                }
            ),
            'img_profile': forms.ClearableFileInput(
                attrs={
                    'class': 'signup-field',
                },
            )
        }


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
