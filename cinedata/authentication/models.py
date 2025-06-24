from django.db import models

# Create your models here.

from movies.models import BaseClass

from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin' , 'Admin'

    USER = 'User' , 'User'

class Profile(AbstractUser):

    role = models.CharField(max_length=10,choices=RoleChoices.choices)

    mobile_num = models.CharField(max_length=10,unique=True)

    def __str__(self):

        return self.email
    
    class Meta :

        verbose_name = 'Profile'

        verbose_name_plural = 'Profile'

class OTP(BaseClass):

    user = models.ForeignKey( 'Profile', on_delete=models.CASCADE)

    otp = models.CharField(max_length=4)

    def __str__(self):

        return f"{self.user.email} - {self.otp}"

    class Meta:

        verbose_name = 'OTP'

        verbose_name_plural = 'OTP'