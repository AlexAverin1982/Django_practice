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
    path("", views.BlogRecordListView.as_view(), name="blog"),
    path("add_record/", views.BlogRecordCreateView.as_view(), name="add_blog_record"),
    path("blog_record/<int:pk>/", views.BlogRecordView.as_view(), name="record_content"),
    path("edit/<int:pk>/", views.BlogRecordUpdateView.as_view(), name="edit_BlogRecord"),
    path("delete/<int:pk>/", views.BlogRecordDeleteView.as_view(), name="delete_BlogRecord"),

]

"""
path("details/<int:pk>/", views.BlogRecordDetailView.as_view(), name="BlogRecord_details"),
path("new_BlogRecord/", views.BlogRecordCreateView.as_view(), name="new_BlogRecord"),
path("edit/<int:pk>/", views.BlogRecordUpdateView.as_view(), name="edit_BlogRecord"),
path("new_category/", views.CategoryCreateView.as_view(), name="new_category"),
path("contacts/", views.ContactsView.as_view(), name="contacts"),
path("feedback/", views.FeedbackFormView.as_view(), name="feedback"),
path("posted_info/<int:pk>/", views.PostedMessageView.as_view(), name="posted_info"),
# path("admin/", admin.site.urls),
# path("", views.home, name="home"),
# path("new_BlogRecord/", views.new_BlogRecord, name="new_BlogRecord"),
# path("contacts/", views.contacts, name="contacts"),
# path("details/<int:BlogRecord_id>", views.details, name="BlogRecord_details"),
# path("new_category/", views.new_category, name="new_category"),
# path("new_category/add", views.add_category, name="add_category"),
# path("new_BlogRecord/add", views.add_BlogRecord, name="add_BlogRecord"),
]

"""
