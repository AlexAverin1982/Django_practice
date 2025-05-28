from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import BlogRecordCreateForm
from blog.models import BlogRecord
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogRecordCreateView(LoginRequiredMixin, generic.CreateView):
    model = BlogRecord
    form_class = BlogRecordCreateForm
    template_name = 'new_record.html'
    success_url = reverse_lazy('blog')
    extra_context = {
        'title': 'Новая запись в блоге',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BlogRecordListView(generic.ListView):
    model = BlogRecord
    template_name = "blog_records.html"
    context_object_name = 'records'
    paginate_by = 50
    extra_context = {
        'show_all': True,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True).order_by("-created_at")

class BlogRecordView(generic.DetailView):
    model = BlogRecord
    template_name = "record_content.html"
    context_object_name = 'record'

    def get_object(self, queryset=None):
        # Переопределение метода get_object для настройки логики выбора объекта
        obj = super().get_object(queryset)
        obj.increment_views_count()
        return obj


class BlogRecordUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = BlogRecord
    form_class = BlogRecordCreateForm
    template_name = 'new_record.html'
    extra_context = {
        'page_title': 'Редактирование записи',
        'editing_mode': True,
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse("product_details", kwargs=self.kwargs)


class BlogRecordDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = BlogRecord
    success_url = reverse_lazy("blog")
    template_name = 'delete_record.html'

