import random

from django.shortcuts import render
from django.http import *
from .forms import AuthorsForm
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Cart
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book


def index(request):
    books = []
    all_books = Book.objects.all()
    while len(books) < 12:
        book = random.choice(all_books)
        if book not in books:
            books.append(book)
    print(books)
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'index.html', context={'num_books': num_books,
                                                  'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors,
                                                  'num_visits': num_visits,
                                                  'books': books[:4],
                                                  'books2': books[4:8],
                                                  'books3': books[8:]})


def cart(request):
    if request.method == "POST":
        if request.POST.get('delete'):
            book = Cart.objects.get(id=request.POST.get('delete'))
            book.delete()
        elif request.POST.get('increment'):
            book = Cart.objects.get(id=request.POST.get('increment'))
            book.quantity = book.quantity + 1
            book.save()
        elif request.POST.get('decrement'):
            book = Cart.objects.get(id=request.POST.get('decrement'))
            if book.quantity > 1:
                book.quantity = book.quantity - 1
                book.save()
        elif request.POST.get('quantity'):
            print(request.POST)
            book = Cart.objects.get(id=request.POST.get('book_id'))
            if int(request.POST.get('book_id')) > 1:
                book.quantity = int(request.POST.get('quantity'))
                book.save()
    cart = Cart.objects.filter(user__exact=request.user.id)
    return render(request, 'catalog/cart.html', context={'cart': cart})


def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")


def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Author not found</h2>")


def edit1(request, id):
    author = Author.objects.get(id=id)

    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        print(author.date_of_birth)
        return render(request, "edit1.html", {"author": author})


def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'catalog/author_add.html', {"form": authorsform, "author": author})


def book_list(request):
    print('GET: ',request.GET)
    print('POST: ', request.POST)
    # print(request.get_full_path())
    # print(dir(request))
    books = Book.objects.all()
    filters = []
    if request.method == 'GET':
        genres_filter = request.GET.getlist('genres')
        authors_filter = request.GET.getlist('authors')
        filters += genres_filter + authors_filter
        genre_id_list = []
        authors_id_list = []
        # books = Book.objects
        if genres_filter:
            for genre in genres_filter:
                try:
                    genre_id_list.append(Genre.objects.get(name=genre))
                except Genre.DoesNotExist:
                    pass
            books = Book.objects.filter(genre__in=genre_id_list)
        if authors_filter:
            for author in authors_filter:
                try:
                    authors_id_list.append(Author.objects.get(first_name=author))
                except Genre.DoesNotExist:
                    pass
                books = books.filter(author__in=authors_id_list)
    genres = Genre.objects.all()
    authors = Author.objects.all()
    paginator = Paginator(books, 9)  # Show 9 books per page.
    is_paginated = True if paginator.num_pages > 1 else False
    page_number = request.GET.get('page')
    print('page_number',page_number)
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)
    # print(page_range)
    return render(request, 'catalog/book_list.html', {'book_list': books,
                                                      'genres': genres,
                                                      'authors': authors,
                                                      'page_obj': page_obj,
                                                      'page_range': page_range,
                                                      'is_paginated': is_paginated,
                                                      'filters': filters
                                                        })


def about_us(request):
    return render(request, 'about_us.html')


class BookListView(generic.ListView):
    model = Book
    paginate_by = 9


class BookDetailView(generic.DetailView):
    model = Book
    # template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get('add_to_cart'):
            cart = Cart()
            cart.books = Book.objects.get(id=request.POST.get('add_to_cart'))
            cart.user = User.objects.get(id=request.POST.get('user'))
            cart.save()
        self.object = self.get_object()
        context = super(BookDetailView, self).get_context_data(**kwargs)
        return self.render_to_response(context=context)


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя. """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='1').order_by('due_back')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
