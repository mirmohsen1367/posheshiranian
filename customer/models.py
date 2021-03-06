from django.db import models
from django.core.validators import RegexValidator


class Company(models.Model):
    name = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    class Meta:
        db_tablespace = "customer_company"

    def __str__(self):
        return self.name
