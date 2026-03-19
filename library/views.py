from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Author, Book
from .forms import AuthorForm, BookForm
from .services import BookService

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


# Create your views here.
class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        if not request.user.has_perm("library.can_review_book"):
            return HttpResponseForbidden("You have no right to refer the book.")

        book.review = request.POST.get("review")
        book.save()

        return redirect("library:book_detail", pk=pk)


class RecommendBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        if not request.user.has_perm("library.can_recommend_book"):
            return HttpResponseForbidden("You have no right to recommend the book.")

        book.recommend = True
        book.save()

        return redirect("library:book_detail", pk=pk)


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class AuthorListView(ListView):
    model = Author
    template_name = "library/authors_list.html"
    context_object_name = "authors"

    def get_queryset(self):
        queryset = cache.get("authors_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("authors_queryset", queryset, 60 * 15)
        return queryset


class AuthorDetailView(DetailView):
    model = Author
    template_name = "library/author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_books_count"] = context["author"].books.count()
        return context


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "library/author_confirm_delete.html"
    success_url = reverse_lazy("library:authors_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    template_name = "library/books_list.html"
    context_object_name = "books"
    permission_required = "library.view_book"

    def get_queryset(self):
        queryset = super().get_queryset()  # Get the default queryset.objects.all()
        return queryset.filter(publication_date__year__gt=2000)


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    # fields = ['title', 'publication_date', 'author']
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.add_book"


@method_decorator(cache_page(60 * 15), name="dispatch")
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context["author_books_count"] = Book.objects.filter(
            author=self.object.author
        ).count()

        book_id = self.object.id
        context["average_rating"] = BookService.calculate_average_rating(book_id)
        context["is_popular"] = BookService.calculate_average_rating(book_id)

        print(context)
        return context


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    # fields = ['title', 'publication_date', 'author']
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.change_book"


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = "library/book_confirm_delete.html"
    success_url = reverse_lazy("library:books_list")
    permission_required = "library.delete_book"


# def books_list(request):
#     books = Book.objects.all()
#     context = {'books': books}
#     return render(request, 'library/books_list.html', context)
#
#
# def book_detail(request, book_id):
#     book = Book.objects.get(id=book_id)
#     context = {'book': book}
#     return render(request, 'library/book_detail.html', context)
