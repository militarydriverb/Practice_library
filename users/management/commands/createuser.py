from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username="testuser",
            email="TestUser@mail.com",
            first_name="Test",
            last_name="User",
        )

        user.set_password("123")

        user.is_staff = True
        user.is_superuser = False

        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"User created successfully with email {user.email}")
        )
