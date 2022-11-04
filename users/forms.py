from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password


def hp_validator(value):
    if len(str(value)) != 10:
        raise forms.ValidationError('정확한 핸드폰 번호를 입력해주세요.')


class CsRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CsRegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'email', 'name', 'hp']

    def save(self, commit=True):
        user = super(CsRegisterForm, self).save(commit=False)
        user.level = '2'
        user.department = '필로티'
        user.is_active = False
        user.save()

        return user
    
class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control', }),
        error_messages={'required':'아이디를 입력해주세요.'},
        max_length=17,
        label='아이디'
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control',}),
        error_messages = {'required':'비밀번호를 입력해주세요.'},
        label = '비밀번호'
        )
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        
        if user_id and password:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
                    
                    
    