from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, phone_number, full_name, password, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            full_name=full_name,
            is_active=True,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        superUser = self.model(email=email, **other_fields)
        superUser.set_password(password)
        superUser.save()
        return superUser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.is_staff == True:
            return f"{self.phone_number}"
        return self.full_name


class Otp(BaseModel):
    user = models.ForeignKey(User, related_name="user_otp", on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    has_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.otp}"
    
class EmergencyInformation(BaseModel):
    
    BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    user = models.ForeignKey(User, related_name="user_emergency", on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP)

    def __str__(self):
        return f"{self.user.full_name} - {self.blood_group}"

class ContactInformation(BaseModel):
    user = models.ForeignKey(User, related_name="user_contact", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.user.full_name} - {self.name} - {self.phone_number}"