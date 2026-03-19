from django.contrib import admin
from .models import Author, Book, Review

# Первый способ регистрации моделей в админке
# admin.site.register(Author)
# admin.site.register(Book)


# Второй (декораторный) способ регистрации моделей в админке
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    # Дополнительные настройки (опционально)
    search_fields = (
        "first_name",
        "last_name",
    )
    list_filter = ("birth_date",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date")
    # Дополнительные настройки (опционально)
    list_filter = ("publication_date", "author")
    search_fields = ("title", "author__first_name", "author__last_name")
    ordering = ("-publication_date",)  # Сортировка по дате (новые сверху)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "rating",
    )
