from django.db import models


class Journalist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    email = models.EmailField()