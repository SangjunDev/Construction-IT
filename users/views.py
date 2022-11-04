import re
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .decorators import *
from .models import User
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import CsRegisterForm
from django.views.generic import CreateView
from django.urls import reverse
from .helper import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView
from django.conf import settings

#로그인
@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)
        
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            remeber_session = self.request.POST.get('remember_session', False)
            if remeber_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                
        return super().form_valid(form)
    
#로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')
        

# 회원가입 약관동의
@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'users/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            if request.POST.get('csregister') == 'csregister':       
                return redirect('/users/csregister/')
            else:
                return redirect('/users/register/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'users/agreement.html')  
        
        
#필로티 이용자 회원가입
class CsRegisterView(CreateView):
    model = User
    template_name = 'users/register_cs.html'
    form_class = CsRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        self.request.session['register_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        return reverse('users:register_success')

    def form_valid(self, form):
        self.object = form.save()
        
        send_mail(
        '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
        [self.object.email],
        html=render_to_string('users/register_email.html', {
            'user': self.object,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
            'domain': self.request.META['HTTP_HOST'],
            'token': default_token_generator.make_token(self.object),
        }),
    )
        return redirect(self.get_success_url())
    
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'users/register_success.html')    

# 이메일 인증 활성화
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('users:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('users:login')

    


