import os

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("library:books_list")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_mail):
        subject = "Welcome to Library"
        message = "Thank you for signing up for your account in our Library."
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [user_mail]
        send_mail(subject, message, from_email, recipient_list)
