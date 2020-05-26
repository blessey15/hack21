from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

GENDER_CHOICES=(
    ('m','Male'),
    ('f','Female'),
    ('n',"Non Binary"),
    ('na', 'Prefer not to say',)
)
T_SHIRT_SIZE_CHOICES=(
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL')
)
FIELD_OF_STUDY_CHOICES=(
    ('cs','Computer Science'),
    ('ec','Electronics and Communication'),
    ('me','Mechanical Engineering'),
    ('ce','Civil Engineering'),
    ('ee','Electrical and Electronis Engineering'),
    ('it','Information Technology')
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    # name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(max_length=256, blank=False, unique=True)
    # contact = models.IntegerField( blank=False)
    # dob = models.DateField()
    # gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
    # bio = models.TextField()
    # tshirt_size = models.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')
    # #emergency conatct
    # skills = models.TextField()
    # educational_institution = models.CharField(max_length= 128)
    # field_of_study = models.CharField(max_length=64, choices=FIELD_OF_STUDY_CHOICES, blank=True, verbose_name='Field of Study')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # is_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

################### HAVE TO MODIFY
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_short_name(self):
        return self.email

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
