from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre", verbose_name="Book genre")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Enter a book language", verbose_name="Book language")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Enter author first name", verbose_name="Author first name")
    last_name = models.CharField(max_length=100, help_text="Enter author last name", verbose_name="Author last name")
    date_of_birth = models.DateField(help_text="Enter a author`s date of birth",
                                     verbose_name="Author date of birth",
                                     null=True,
                                     blank=True)
    date_of_death = models.DateField(help_text="Enter a author`s date of death",
                                     verbose_name="Author date of death",
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Enter a book name",
                             verbose_name="Book name")
    price = models.FloatField(help_text="Enter price of this book",
                              verbose_name='Book price',
                              default=0)
    genre = models.ForeignKey('Genre',
                              on_delete=models.CASCADE,
                              help_text="Enter a book genre",
                              verbose_name="Book genre", null=True)
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE,
                                 help_text="Enter a book language",
                                 verbose_name="Book language", null=True)
    author = models.ManyToManyField('Author',
                                    help_text="Enter author",
                                    verbose_name="Book author")
    summary = models.TextField(max_length=1000,
                               help_text="Enter description of this book",
                               verbose_name='Book summary')
    isbn = models.CharField(max_length=13,
                            help_text="Must be 13 symbols in length")

    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Authors'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_image(self):
        return f'/media/{self.image}/'


class Cart(models.Model):
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                )
    books = models.ForeignKey(Book,
                              on_delete=models.CASCADE,)
    quantity = models.IntegerField('quantity',
                                   blank=False,
                                   default=1,
                                   help_text='Quantity books in order')


class Status(models.Model):
    name = models.CharField(max_length=20, help_text="Enter a book status", verbose_name="Book status")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    ivn_nom = models.CharField(max_length=20,
                               null=True,
                               help_text="Enter the inventory number of the book",
                               verbose_name="Inventory number")
    imprint = models.CharField(max_length=200,
                               null=True,
                               help_text="Enter publisher and year of release",
                               verbose_name="Publisher")
    status = models.ForeignKey('Status',
                               on_delete=models.CASCADE,
                               null=True,
                               help_text='Edit a book status',
                               verbose_name="Book status")
    due_back = models.DateField(null=True,
                                blank=True,
                                help_text="Enter status expiration date",
                                verbose_name="Expiration date")
    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name="Customer",
                                 help_text="Select book customer")

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f"{self.ivn_nom} {self.book} {self.status}"
