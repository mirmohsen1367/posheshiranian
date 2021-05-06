from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from customer.models import Company


class CustomAcountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):  # creating super user method

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.setdefault('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is stuff=True")
        if other_fields.setdefault('is_active') is not True:
            raise ValueError("Superuser must be assigned to is active=True")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('you must provide emaile address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CUser(AbstractBaseUser, PermissionsMixin):
    """ this is my custom user  """
    GENDER = [
        ('MALE', 'male'),
        ('FEMALE', 'female')
    ]

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']
    companies = models.ManyToManyField('customer.Company', through="customer.Evalution")

    objects = CustomAcountManager()

    class Meta:
        db_table = "user_user"


    def __str__(self):
        return self.user_name

class Insurer(models.Model):
    insurer_start = models.DateField(timezone.now(), null=True)
    insurer_end = models.DateField(timezone.now(), null=True)
    user = models.OneToOneField(CUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user_name

class EvaluationExpert(models.Model):
    user = models.OneToOneField(CUser, on_delete=models.CASCADE)


    class Meta:
        db_table = 'user_evaluation_expert'

    def __str__(self):
        return self.user.user_name
