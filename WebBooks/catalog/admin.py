from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class AdminBookInstance(admin.ModelAdmin):
    list_filter = ('book', 'status')



