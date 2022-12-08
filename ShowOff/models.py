from django.db import models
from Base.models import User
# Create your models here.
class Categorie(models.Model):
  name = models.CharField(max_length=10000)
  slug = models.SlugField(max_length=250, unique=True)

  def __str__(self):
    return self.name


class Contributors(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  show_off = models.ForeignKey(ShowOff, on_delete=models.CASCADE)


  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user

class Support(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  show_off = models.ForeignKey(ShowOff, on_delete=models.CASCADE)


  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user

class Rating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  show_off = models.ForeignKey(ShowOff, on_delete=models.CASCADE)
  rating = models.PositiveIntegerField(default=0)
  comment = models.TextField()

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user


class ShowOff(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=1000000)
  slug = models.SlugField(max_length=1000000, unique=True)
  url = models.URLField()
  body = models.TextField()
  category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)

  # The Connection field between ShowOff and Them
  contributors = models.ForeignKey(Contributors, on_delete=models.SET_NULL, null=True)
  support = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True)
  rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True)

  
  featured_image = models.ImageField(upload_to="Featured_Image/")

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)

      if not self.id:
        try:
          points = settings.POINTS_SETTINGS['CREATE_SHOWOFFS']
        except KeyError:
          points = 0
        User.objects.get(id=self.user_id).modify_points(points)
      return super(ShowOff, self).save(*args, **kwargs)

class ShowOffComment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  show_off = models.ForeignKey(ShowOff, on_delete=models.CASCADE)
  comment = models.TextField()

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.comment