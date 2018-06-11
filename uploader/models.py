from django.db import models


class ImageUploader(models.Model):
    image = models.ImageField(upload_to='images/')
    filename = models.CharField(primary_key=True, max_length=100)
