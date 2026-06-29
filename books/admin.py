from django.contrib import admin
from .models import Author, Genre, Book

admin.site.register(Author)
admin.site.register(Book)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Эта фишка заставит Django автоматически писать слаг на английском, пока ты пишешь имя жанра!
    prepopulated_fields = {'slug': ('name',)}