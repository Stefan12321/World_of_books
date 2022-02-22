import datetime

from django.test import TestCase
from catalog.models import Author, Genre, Book, Language, Cart, Status, BookInstance
from django.contrib.auth.models import User
from datetime import date


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'Author first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'Author last name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Author date of death')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'Author date of birth')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = author.last_name
        self.assertEquals(expected_object_name, str(author))

    # def test_get_absolute_url(self):
    #     author=Author.objects.get(id=1)
    #     #This will also fail if the urlconf is not defined.
    #     self.assertEquals(author.get_absolute_url(),'/catalog/author/1')


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Test genre")

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_genre_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Book genre')

    def test_object_name_is_genre_name(self):
        genre = Genre.objects.get(id=1)
        expected_object_name = genre.name
        self.assertEquals(expected_object_name, str(genre))


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name="Test Language")

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_Language_name(self):
        language = Language.objects.get(id=1)
        expected_object_name = language.name
        self.assertEquals(expected_object_name, str(language))


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Test genre")
        Author.objects.create(first_name='Big', last_name='Bob')
        author = Author.objects.get(first_name='Big')
        book = Book.objects.create(title="Test book",
                                   price=20,
                                   genre=Genre.objects.get(name="Test genre"),
                                   summary="Test summary",
                                   isbn="testisbn",
                                   image='images/The_Adventures_of_Sherlock_Holmes_4YcB5Vc.jpg')
        book.author.add(author)

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEquals(max_length, 13)

    def test_title_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('title').verbose_name
        self.assertEquals(verbose_name, "Book name")

    def test_price_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('price').verbose_name
        self.assertEquals(verbose_name, "Book price")

    def test_genre_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('genre').verbose_name
        self.assertEquals(verbose_name, "Book genre")

    def test_language_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('language').verbose_name
        self.assertEquals(verbose_name, "Book language")

    def test_author_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('author').verbose_name
        self.assertEquals(verbose_name, "Book author")

    def test_summary_verbose_name(self):
        book = Book.objects.get(id=1)
        verbose_name = book._meta.get_field('summary').verbose_name
        self.assertEquals(verbose_name, "Book summary")

    def test_display_author(self):
        book = Book.objects.get(id=1)
        display_author = book.display_author()
        self.assertEquals(display_author, 'Bob')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        url = book.get_absolute_url()
        self.assertEquals(url, '/book/1')

    def test_get_image(self):
        book = Book.objects.get(id=1)
        image = book.get_image()
        self.assertEquals(image, '/media/images/The_Adventures_of_Sherlock_Holmes_4YcB5Vc.jpg/')

    def test_object_name_is_book_title(self):
        book = Book.objects.get(id=1)
        title = book.title
        self.assertEquals(title, str(book))


# class CartModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         User.objects.create_user(username="Test_username")
#         Genre.objects.create(name="Test genre")
#         Author.objects.create(first_name='Big', last_name='Bob')
#         author = Author.objects.get(first_name='Big')
#         book_instance = Book.objects.create(title="Test book",
#                                             price=20,
#                                             genre=Genre.objects.get(name="Test genre"),
#                                             summary="Test summary",
#                                             isbn="testisbn",
#                                             image='images/The_Adventures_of_Sherlock_Holmes_4YcB5Vc.jpg')
#         book_instance.author.add(author)
#         Cart.objects.create(user=User.objects.get(id=1),
#                             books=Book.objects.get(id=1),
#                             quantity=1)
#
#     def test

class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name="Test status")

    def test_name_max_length(self):
        status = Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_status_name(self):
        status = Status.objects.get(id=1)
        name = status.name
        self.assertEquals(name, str(name))


class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="Test_username")
        Genre.objects.create(name="Test genre")
        Status.objects.create(name="Test status")
        Author.objects.create(first_name='Big', last_name='Bob')
        author = Author.objects.get(first_name='Big')
        book = Book.objects.create(title="Test book",
                                   price=20,
                                   genre=Genre.objects.get(name="Test genre"),
                                   summary="Test summary",
                                   isbn="testisbn",
                                   image='images/The_Adventures_of_Sherlock_Holmes_4YcB5Vc.jpg')
        book.author.add(author)
        BookInstance.objects.create(book=Book.objects.get(id=1),
                                    ivn_nom="1",
                                    imprint="Test imprint",
                                    status=Status.objects.get(id=1),
                                    borrower=User.objects.get(id=1)
                                    )

    def test_ivn_nom_max_length(self):
        book_instance = BookInstance.objects.get(id=1)
        max_length = book_instance._meta.get_field('ivn_nom').max_length
        self.assertEquals(max_length, 20)

    def test_imprint_max_length(self):
        book_instance = BookInstance.objects.get(id=1)
        max_length = book_instance._meta.get_field('imprint').max_length
        self.assertEquals(max_length, 200)

    def test_ivn_nom_verbose_name(self):
        book_instance = BookInstance.objects.get(id=1)
        verbose_name = book_instance._meta.get_field('ivn_nom').verbose_name
        self.assertEquals(verbose_name, 'Inventory number')

    def test_imprint_verbose_name(self):
        book_instance = BookInstance.objects.get(id=1)
        verbose_name = book_instance._meta.get_field('imprint').verbose_name
        self.assertEquals(verbose_name, 'Publisher')

    def test_status_verbose_name(self):
        book_instance = BookInstance.objects.get(id=1)
        verbose_name = book_instance._meta.get_field('status').verbose_name
        self.assertEquals(verbose_name, 'Book status')

    def test_due_back_verbose_name(self):
        book_instance = BookInstance.objects.get(id=1)
        verbose_name = book_instance._meta.get_field('due_back').verbose_name
        self.assertEquals(verbose_name, 'Expiration date')

    def test_borrower_verbose_name(self):
        book_instance = BookInstance.objects.get(id=1)
        verbose_name = book_instance._meta.get_field('borrower').verbose_name
        self.assertEquals(verbose_name, 'Customer')

    def test_is_overdue(self):
        book_instance = BookInstance.objects.get(id=1)
        book_instance.due_back = date.today() - datetime.timedelta(days=2)
        self.assertTrue(book_instance.is_overdue)

    def test_not_is_overdue(self):
        book_instance = BookInstance.objects.get(id=1)
        book_instance.due_back = date.today() + datetime.timedelta(days=2)
        self.assertFalse(book_instance.is_overdue)

    def test_object_name_is_ibn_num_and_book_and_status(self):
        book_instance = BookInstance.objects.get(id=1)
        object_name = f'{book_instance.ivn_nom} {book_instance.book} {book_instance.status}'
        self.assertEquals(object_name, str(book_instance))
