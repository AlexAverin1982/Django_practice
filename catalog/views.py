from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.urls import reverse_lazy
from .models import ContactsInfo, Product, Category, FeedbackMessage
from django.conf import settings
from django.core.mail import send_mail
from .forms import ProductCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from typing_extensions import Any
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = 'product'


class ProductListView(generic.ListView):
    model = Product
    template_name = "home.html"
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.order_by("-created_at")


class ProductCreateView(
    generic.CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'categories': Category.objects.all().order_by('name'),
        'title': 'Добавление товара',
    }

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        return super(ProductCreateView, self).post(request, **kwargs)


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'categories': Category.objects.all().order_by('name'),
        'title': 'Редактирование товара',
        'product_editing_mode': True,
    }

    def post(self, request, *args, **kwargs) -> Any:
        # уточнить, изменяется ли статус публикации
        form = self.get_form()
        print(form)
        if 'is_published' in form.changed_data:
            if not request.user.has_perm('catalog.can_unpublish_product'):
                return HttpResponseForbidden("У вас нет прав для изменения статуса публикаци товара")

        # super(generic.UpdateView).post(request, *args, **kwargs)
        return super(ProductUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("product_details", kwargs=self.kwargs)


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'new_category.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Добавление категории',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactsView(generic.TemplateView):
    model = ContactsInfo
    template_name = "contacts.html"
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contacts': ContactsInfo.objects.order_by("-updated_at")[0],
            'title': 'Наши контакты',
        })
        return context


class PostedMessageView(generic.DetailView):
    model = FeedbackMessage
    template_name = "response.html"
    context_object_name = 'message'


class FeedbackFormView(generic.CreateView):
    model = FeedbackMessage
    fields = ['name', 'email', 'message']
    template_name = 'feedback.html'

    def form_valid(self, form):
        new_message = form.save()
        return HttpResponseRedirect(reverse('posted_info', args=(new_message.pk,)))


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("home")
    template_name = 'delete_product.html'

    def post(self, request, *args, **kwargs) -> Any:
        obj = Product.objects.get(id=kwargs['pk'])
        if (not request.user.has_perm('catalog.delete_product')) and (obj.owner != request.user):
            return HttpResponseForbidden("У вас нет прав для удаления товара")

        super(ProductDeleteView, self).post(request, *args, **kwargs)

        return redirect('home')


def send_letter(request) -> None:
    send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL])
    return render(request, "home.html")
