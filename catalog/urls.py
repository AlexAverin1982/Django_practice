"""
URL configuration for catalog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("details/<int:pk>/", views.ProductDetailView.as_view(), name="product_details"),
    path("new_product/", views.ProductCreateView.as_view(), name="new_product"),
    path("edit/<int:pk>/", views.ProductUpdateView.as_view(), name="edit_product"),
    path("new_category/", views.CategoryCreateView.as_view(), name="new_category"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("feedback/", views.FeedbackFormView.as_view(), name="feedback"),
    path("posted_info/<int:pk>/", views.PostedMessageView.as_view(), name="posted_info"),
    # path("admin/", admin.site.urls),
    # path("", views.home, name="home"),
    # path("new_product/", views.new_product, name="new_product"),
    # path("contacts/", views.contacts, name="contacts"),
    # path("details/<int:product_id>", views.details, name="product_details"),
    # path("new_category/", views.new_category, name="new_category"),
    # path("new_category/add", views.add_category, name="add_category"),
    # path("new_product/add", views.add_product, name="add_product"),
]

