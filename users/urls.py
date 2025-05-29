from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, UserProfileView, UserDeleteView, UserUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('greetings/<int:pk>', RegisterView.as_view(), name='greetings'),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user_profile"),
    path('edit_user/<int:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path("delete_user/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
]