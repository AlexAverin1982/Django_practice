from django.urls import path

from . import views

urlpatterns = [
    path("", views.BlogRecordListView.as_view(), name="blog"),
    path("add_record/", views.BlogRecordCreateView.as_view(), name="add_blog_record"),
    path("blog_record/<int:pk>/", views.BlogRecordView.as_view(), name="record_content"),
    path("edit/<int:pk>/", views.BlogRecordUpdateView.as_view(), name="edit_BlogRecord"),
    path("delete/<int:pk>/", views.BlogRecordDeleteView.as_view(), name="delete_BlogRecord"),
]
