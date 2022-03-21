from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,first_name,last_name,date_of_birth,phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth,phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name,last_name,date_of_birth,phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,first_name,last_name,date_of_birth,phone_number, password, **extra_fields)

    def create_superuser(self, email,first_name,last_name,date_of_birth,phone_number, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault("user_type", 'CUSTOMER')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must be assigned to is_active=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,first_name,last_name,date_of_birth,phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # USER_TYPE_CHOICES = (
    #   ('VENDOR', 'Vendor'),
    #   ('CUSTOMER', 'Customer'),
      
    # )
    email = models.EmailField(_('email address'), unique=True)
    # user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=15, default='CUSTOMER')
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    phone_number = PhoneNumberField(blank=True)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    
    #superuser fields
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(_('active'), default=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','date_of_birth','phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)