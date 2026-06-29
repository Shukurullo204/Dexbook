from django.db import models
from django.conf import settings

from books.models import Book

class ReadingProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.IntegerField()
    percent = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

class BookShelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    books = models.ManyToManyField(Book,blank=True)

    def __str__(self):
        return f"Полка '{self.name}' пользователя {self.user.email}"
