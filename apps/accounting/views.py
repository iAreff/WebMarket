from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext
from .forms import ForgetPasswordForm, PasswordChangeForm, UserRegisterationForm, VerifyRegisterationForm, UserLoginForm
from .models import CustomUser
from utils import createRandomCode, sendSMS


class UserRegisterationView(View):
    template_name = 'accounting/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request,*args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        form = UserRegisterationForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            activation_code = createRandomCode()
            CustomUser.objects.create_user(
                mobile = data['mobile'],
                activation_code = activation_code,
                password = data['password2'])
            sendSMS(data['mobile'],f'کد فعال سازی: {activation_code}')
            request.session['user_session'] = {
                'activation_code' : str(activation_code),
                'mobile' : data['mobile'],
                'forget_password': False}
            messages.success(request,gettext('Verify code has sent to your mobile number'),'success')
            return redirect('accounting:verify_registeration')
        
        messages.error(request,gettext('Error'),'danger')
        

class VerifyRegisterationView(View):
    template_name = 'accounting/verify_registeration.html'
    
    def get(self,request,*args,**kwargs):
        form = VerifyRegisterationForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = VerifyRegisterationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            
            if data['activation_code'] == user_session['activation_code']:
                user = CustomUser.objects.get(mobile=user_session['mobile'])
                
                if not user_session['forget_password']:
                    user.is_active = True
                    user.activation_code = createRandomCode()
                    user.save()
                    messages.success(request,gettext('Congratulations, Your Sign Up is Done'),'success')
                    return redirect('main:index')
                else:
                    return redirect('accounting:password_change')
        
            else:
                messages.error(request,gettext('Wrong code!'),'danger')
                return render(request,self.template_name,{'form':form})
        
        messages.error(request,gettext('Enter correct data please!'),'danger')
        return render(request,self.template_name,{'form':form})


class UserLoginView(View):
    template_name = 'accounting/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request,*args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        form = UserLoginForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['mobile'],password=data['password'])
            
            if user is not None:
                temp = CustomUser.objects.get(mobile=data['mobile'])
                
                if not temp.is_admin:
                    messages.success(request,'شما وارد شدید','success')
                    login(request,user)
                    next_url = request.GET.get('next')
                    
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                
                else:
                    messages.error(request,'ادمین نمی تواند از این جا وارد شود','warning')
                    return render(request,self.template_name,{'form':form})
                
            else:
                messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
                return render(request,self.template_name,{'form':form})
        
        else:
            messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
            return render(request,self.template_name,{'form':form})
            
            
class UserLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request,*args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('main:index')
    

class UserPanelView(LoginRequiredMixin,View):
    template_name = 'accounting/user_panel.html'
    
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)


class PasswordChangeView(View):
    template_name = 'accounting/password_change.html'
    
    def get(self,request,*args,**kwargs):
        form = PasswordChangeForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = PasswordChangeForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = CustomUser.objects.get(mobile=user_session['mobile'])
            user.set_password(data['password1'])
            user.activation_code = createRandomCode()
            user.save()
            messages.success(request,'رمز عبور شما با موفقیت تغییر کرد','success')
            return redirect('accounting:login')
        
        else:
            messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
            return render(request,self.template_name,{'form':form})
            

class ForgetPasswordView(View):
    template_name = 'accounting/forget_password.html'
    
    def get(self,request,*args,**kwargs):
        form = ForgetPasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = ForgetPasswordForm(request.POST)
        
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = CustomUser.objects.get(mobile=data['mobile'])
                activation_code = createRandomCode()
                user.activation_code = activation_code
                user.save()
                sendSMS(data['mobile'],f'کد احراز هویت: {activation_code}')
                request.session['user_session'] = {
                    'activation_code' : str(activation_code),
                    'mobile' : data['mobile'],
                    'forget_password' : True}
                messages.success(request,'کد احراز هویت به شماره موبایل شما ارسال شد','success')
                return redirect('accounting:verify_registeration')
            
            except:
                messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
                return render(request,self.template_name,{'form':form})

