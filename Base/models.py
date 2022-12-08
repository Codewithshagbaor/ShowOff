from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.template.defaultfilters import slugify
# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, name, email, user_type, password):
    if not email:
      raise ValueError('Email Needed')

    user = self.model(
      name=name,
      email=self.normalize_email(email),
    )
    if user_type == 'cooperate':
      user.is_cooperate = True
    elif user_type == 'personal':
      user.is_personal = True
    else:
      raise ValueError('User type Needed')
      user.set_password(password)
      user.save(self._db)
      return user

  def create_superuser(self, name, email, password):
    if not email:
      raise ValueError('Email Needed')

    user = self.model(
      name=name,
      email=self.normalize_email(email),
    )
    user.is_admin = True
    user.set_password(password)
    user.save(self._db)
    return user

class Categorie(models.Model):
  name = models.CharField(max_length=10000)
  slug = models.SlugField(max_length=250, unique=True)

  def __str__(self):
    return self.name
      
class User(AbstractUser):
  email = models.EmailField(
    verbose_name='Email Address',
    max_length=255,
    unique=True,
  )
  is_active = models.BooleanField(default=True)
  is_cooperate = models.BooleanField(default=False)
  is_personal = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  username = models.CharField(max_length=100)
  name = models.CharField(max_length=1000, null=False)
  bio = models.TextField()
  location = models.CharField(max_length=1000)
  capacity = models.PositiveIntegerField(default=0)
  points = models.PositiveIntegerField(default=0, verbose_name="reputation")
  followers = models.ManyToManyField("self", symmetrical=False, blank=True)
  profile_img = models.ImageField(upload_to='ProfilePicture/', null=True)
  logo = models.ImageField(upload_to='Logos/', null=True)

  USERNAME_FIELD = 'email'

  REQUIRED_FIELDS = ['name']

  objects = UserManager()

  @property
  def is_staff(self):
    return self.is_admin

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  def modify_points(self, added_points):
    self.points += added_points
    self.save()

  def __str__(self):
    return self.username

class Verification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  overview = models.TextField()
  file = models.FileField(upload_to='VerificationFiles/')

  def __str__(self):
    return self.user.name

