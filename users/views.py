from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, DeleteView
from .forms import CustomUserCreationForm
from .models import CustomUser

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = 'user'
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("home")
    template_name = 'delete_user.html'

