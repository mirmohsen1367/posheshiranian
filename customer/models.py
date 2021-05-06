from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Company(models.Model):
    name = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        db_tablespace = "customer_company"

    def __str__(self):
        return self.name




class Evalution(models.Model):
    location = models.CharField(max_length=30)
    user = models.ForeignKey('user.CUser', related_name='ev_expeter',
                                 on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    evalution_time = models.DateTimeField()

    class Meta:
        db_tablespace = "customer_evalution"

    def __str__(self):
        return f"{self.user.user_name} - {self.company.name}"
