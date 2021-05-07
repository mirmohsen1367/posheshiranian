from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from customer.models import Company


class CustomAcountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):  # creating super user method

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.setdefault('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is stuff=True")
        if other_fields.setdefault('is_active') is not True:
            raise ValueError("Superuser must be assigned to is active=True")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('you must provide emaile address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
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
    username = models.CharField(max_length=150,unique=True, default='test')
    name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', 'user_name']
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email', "gender"]
    companies = models.ManyToManyField('customer.Company',
                                       through="user.Evalution")

    permissions = models.ManyToManyField('user.Permission',
                                       through="user.UserPermission")
    objects = CustomAcountManager()

    class Meta:
        db_table = "user_user"


    def __str__(self):
        return self.username


class Insurer(models.Model):
    insurer_start = models.DateField(null=True)
    insurer_end = models.DateField(null=True)
    user = models.OneToOneField(CUser, on_delete=models.CASCADE, null=True, related_name='user_insurer')

    def __str__(self):
        return self.user.username

class EvaluationExpert(models.Model):
    user = models.OneToOneField(CUser, on_delete=models.CASCADE, null=True, related_name='uer_evaluation_expert')


    class Meta:
        db_table = 'user_evaluation_expert'

    def __str__(self):
        return self.user.username


class Permission(models.Model):
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_permission"

    def __str__(self):
        return self.name


class UserPermission(models.Model):

    user =models.ForeignKey(CUser, on_delete=models.CASCADE, related_name='user_cpermissions', default=1)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='cpermission_users', default=1)
    class Meta:
        db_table = "user_permission_user"

class Evalution(models.Model):
    location = models.CharField(max_length=30)
    user = models.ForeignKey('user.CUser', related_name='ev_expeter',
                                 on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    evalution_time = models.DateTimeField()

    class Meta:
        db_tablespace = "user_evalution"

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"
