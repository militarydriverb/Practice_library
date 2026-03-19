from django.urls import path

from library.views import (
    BookListView,
    BookDetailView,
    BookDeleteView,
    BookUpdateView,
    BookCreateView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorListView,
    AuthorDetailView,
    AuthorDeleteView,
    RecommendBookView,
    ReviewBookView,
)

# from .views import books_list, book_detail

app_name = "library"

urlpatterns = [
    path("author/new/", AuthorCreateView.as_view(), name="author_create"),
    path("author/update/<int:pk>/", AuthorUpdateView.as_view(), name="author_update"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
    path("authors/", AuthorListView.as_view(), name="authors_list"),
    path("author/delete/<int:pk>/", AuthorDeleteView.as_view(), name="author_delete"),
    # path('books_list/', books_list, name='books_list'),
    # path('book_detail/<int:book_id>', book_detail, name='book_detail'),
    path("books/", BookListView.as_view(), name="books_list"),
    path("books/create/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/update/<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("book/delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
    path(
        "book/recommend/delete/<int:pk>/",
        RecommendBookView.as_view(),
        name="book_recommend",
    ),
    path("book/review/delete/<int:pk>/", ReviewBookView.as_view(), name="book_review"),
]
