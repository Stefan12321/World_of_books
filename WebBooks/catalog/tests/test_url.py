import unittest
from django.test import Client, TestCase
from catalog.models import Book, Genre, Author
from django.contrib.auth.models import User


class URLTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username="admen", password="1234")
        Genre.objects.create(name="Test genre")
        Author.objects.create(first_name='Big', last_name='Bob')
        author = Author.objects.get(first_name='Big')
        book = Book.objects.create(title="Test book",
                                            genre=Genre.objects.get(name="Test genre"),
                                            summary="Test summary",
                                            isbn="testisbn")
        book.author.add(author)

    def setUp(self):
        # Every test needs a client.
        # self.client = Client()
        self.client.login(username="admen", password="1234")

    # def test_home_page(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = self.client.get('/sign_up/?next=/')
        self.assertEqual(response.status_code, 200)

    def test_books(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    def test_about_us(self):
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)

    def test_book(self):
        response = self.client.get('/book/1')
        self.assertEqual(response.status_code, 200)

    def test_authors(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_authors_add(self):
        response = self.client.get('/authors_add/')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        response = self.client.get('/book/create/')
        self.assertEqual(response.status_code, 200)

    def test_cart(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
