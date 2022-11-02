from django.forms import CharField, Form, ModelForm, PasswordInput, TextInput, ValidationError
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext


class UserCreationForm(ModelForm):
    password1 = CharField(label='password',widget = PasswordInput)
    password2 = CharField(label='confirm password',widget = PasswordInput)
    
    class Meta:
        model=CustomUser
        fields=['mobile','email']

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError(gettext('Passwords are not same'))
        
        return pass2

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
        return user


class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField(help_text=gettext("<a href='../password'>Change Password<a>"))
    
    class Meta:
        model = CustomUser
        fields = ['mobile','email','name','family','gender','password','is_active','is_admin']
    

class UserRegisterationForm(ModelForm):
    password1 = CharField(label='رمز عبور',
                          error_messages={'required':gettext("can't be empty")},
                          widget = PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    password2 = CharField(label='تکرار رمز عبور',
                          error_messages={'required':gettext("can't be empty")},
                          widget = PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}))
    
    class Meta:
        model = CustomUser
        fields = ['mobile']
        widgets = {
            'mobile': TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'})
        }
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError(gettext('Passwords are not same'))
        
        return pass2


class VerifyRegisterationForm(Form):
    activation_code = CharField(label='کد فعال سازی',
                                error_messages={'required':gettext("can't be empty")},
                                widget=TextInput(attrs={'class':'form-control','placeholder':'کد فعال سازی را وارد کنید'}))
    

class UserLoginForm(Form):
    mobile = CharField(label='شماره موبایل',
                                error_messages={'required':gettext("can't be empty")},
                                widget=TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))
    
    password = CharField(label='رمز عبور',
                                error_messages={'required':gettext("can't be empty")},
                                widget=PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    
    
class PasswordChangeForm(Form):
    password1 = CharField(label='رمز عبور',
                          error_messages={'required':gettext("can't be empty")},
                          widget = PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    
    password2 = CharField(label='تکرار رمز عبور',
                          error_messages={'required':gettext("can't be empty")},
                          widget = PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}))
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError(gettext('Passwords are not same'))
        
        return pass2


class ForgetPasswordForm(Form):
    mobile = CharField(label='شماره موبایل',
                                error_messages={'required':gettext("can't be empty")},
                                widget=TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))