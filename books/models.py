from django.db import models
from django.db.models import SET_NULL


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.name




class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,null=True,blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    file = models.FileField(upload_to='books/files')
    cover = models.ImageField(upload_to='books/covers', blank=True)
    def __str__(self):
        return self.title



