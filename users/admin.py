from django.contrib import admin
from .models import CustomUser

# admin.site.register(CustomUser)


@admin.register(CustomUser)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ("password",)
