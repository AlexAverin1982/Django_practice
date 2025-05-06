from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import F

from blog.models import BlogRecord


class BlogRecordCreateView(generic.CreateView):
    model = BlogRecord
    fields = ['title', 'text', 'preview']
    template_name = 'new_record.html'
    success_url = reverse_lazy('blog')
    extra_context = {
        'title': 'Новая запись в блоге',
    }

    def form_valid(self, form):
        form.save()
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
        # q = self.request.GET.get('filter', '')
        # if not q:
        #     return self.model.objects.all()
        return self.model.objects.order_by("-created_at")

        # return self.model.objects.order_by("name")


class BlogRecordView(generic.DetailView):
    model = BlogRecord
    template_name = "record_content.html"
    context_object_name = 'record'

    def get_object(self, queryset=None):
        # Переопределение метода get_object для настройки логики выбора объекта
        obj = super().get_object(queryset)
        # Дополнительная логика (например,  изменения значений полей)
        # if not obj.is_active:
        #     raise Http404("Object not found")
        obj.increment_views_count()
        return obj
    

class BlogRecordUpdateView(generic.UpdateView):
    model = BlogRecord
    fields = ['title', 'preview', 'text', 'is_published']
    template_name = 'new_record.html'
    success_url = reverse_lazy('blog')
    extra_context = {
        'page_title': 'Редактирование записи',
        'editing_mode': True,
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

