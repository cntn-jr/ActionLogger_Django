from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator, RegexValidator

# Create your models here.
class SiteUserManager(BaseUserManager):
    def create_user(self, userId, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not userId:
            raise ValueError('Users must have an email address')

        user = self.model(
            userId=userId,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            userId=userId,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class SiteUser(AbstractBaseUser):
    userId_regix=RegexValidator(regex='^[0-9]{4-10}$')
    userId = models.CharField(
        primary_key=True,
        # validators=[userId_regix],
        max_length=10,
    )
    firstName=models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    lastName=models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    address=models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    tel_regex=RegexValidator(regex='^[0-9]{2,4}-[0-9]{2,4}-[0-9]{3,4}$')
    tel=models.CharField(
        max_length=20,
        validators=[tel_regex],
        null=True,
        blank=True,
    )
    email=models.EmailField(
        max_length=30,
        blank=True,
    )
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects=SiteUserManager()

    USERNAME_FIELD= 'userId'

    def __str__(self):
        return self.userId

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin