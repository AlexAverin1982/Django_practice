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
    path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("send_letter/", views.send_letter, name="send_letter"),
    path("category_products/<int:pk>/", views.CategoryProductsListView.as_view(), name="category_products"),

]

