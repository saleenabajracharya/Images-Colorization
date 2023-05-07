from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os

from django.conf import settings
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

class Post(models.Model):
    title = models.CharField(max_length = 200)
    # content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

    def get_colorized_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            filename = os.path.splitext(os.path.basename(self.image.name))[0]
            colorized_image_name = f'{filename}_colorized.jpg'
            return os.path.join(settings.MEDIA_URL, colorized_image_name)

