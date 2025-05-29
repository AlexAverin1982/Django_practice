from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic import DetailView, DeleteView, UpdateView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = 'user'
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("home")
    template_name = 'delete_user.html'


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'register.html'

    extra_context = {
        'User_editing_mode': True,
    }

    # def __init__(self):
    #     super().__init__()

    def get_success_url(self):
        return reverse("user_profile", kwargs=self.kwargs)
