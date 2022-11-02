from django.db.models import BooleanField, CharField, DateField, EmailField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, email='', name='', family='', activation_code=None, gender=None, password=None):
        
        if not mobile:
            raise ValueError(gettext('Please Enter your phone number'))

        user = self.model(
            mobile=mobile,
            email=self.normalize_email(email),
            name=name,
            family=family,
            activation_code=activation_code,
            gender=gender)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, mobile, email, name, family, activation_code=None, gender=None, password=None):

        user = self.create_user(
            mobile=mobile,
            email=email,
            name=name,
            family=family,
            activation_code=activation_code,
            gender=gender,
            password=password)

        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile = CharField(max_length=11, unique=True,verbose_name='شماره موبایل')
    email = EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    name = CharField(max_length=50, blank=True,verbose_name='نام')
    family = CharField(max_length=50, blank=True,verbose_name='نام خانوادگی')
    GENDER_CHOICES = ((True, gettext('Male')), (False, gettext('Female')))
    gender = BooleanField(max_length=3, blank=True, null=True, choices=GENDER_CHOICES,verbose_name='جنسیت')
    register_date = DateField(auto_now_add=True)
    activation_code = CharField(max_length=100, null=True, blank=True)
    is_active = BooleanField(default=False,verbose_name='وضعیت: فعال/غیرفعال')
    is_admin = BooleanField(default=False,verbose_name='ادمین')

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'name', 'family']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.name + ' ' + self.family
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر‌ها'
        db_table = 'table_user'

    @property
    def is_staff(self):
        return self.is_admin
