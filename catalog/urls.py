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
    # path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/posted_info", views.posted_info, name="posted_info"),
    path("details/<int:pk>/", views.ProductDetailView.as_view(), name="product_details"),
    # path("details/<int:product_id>", views.details, name="details"),
    path("new_category/", views.new_category, name="new_category"),
    path("new_category/add", views.add_category, name="add_category"),
    path("new_product/", views.new_product, name="new_product"),
    path("new_product/add", views.add_product, name="add_product"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
