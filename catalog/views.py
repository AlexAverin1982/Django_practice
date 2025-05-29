from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.urls import reverse_lazy

from users.models import CustomUser
from .models import ContactsInfo, Product, Category, FeedbackMessage
from django.conf import settings
from django.core.mail import send_mail
from .forms import ProductCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from typing_extensions import Any
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from .services import ProductService


def is_moder(user) -> bool:
    if isinstance(user, AnonymousUser):
        return False
    else:
        return user.groups.filter(name='Модераторы продуктов').exists()


def is_superuser(user) -> bool:
    if isinstance(user, AnonymousUser) or isinstance(user, CustomUser):
        return False
    else:
        return user.filter(is_superuser=True).exists()


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = 'product'


class ProductListView(generic.ListView):
    model = Product
    template_name = "home.html"
    context_object_name = 'items'
    paginate_by = 5

    extra_context = {
        'categories': Category.objects.all().order_by('name'),
    }
    def get_queryset(self):
        queryset = cache.get('products_queryset')
        if not queryset:
            user = self.request.user
            if is_moder(user) or is_superuser(user):
                products = self.model.objects.all()
            else:
                products = self.model.objects.filter(is_published=True)
            queryset = products.order_by("-created_at")
            cache.set('products_queryset', queryset, 60 * 15)
        return queryset


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'categories': Category.objects.all().order_by('name'),
        'title': 'Добавление товара',
    }


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
        obj = Product.objects.get(id=kwargs['pk'])
        if obj.owner != request.user:
            return HttpResponseForbidden("У вас нет прав для изменения свойств товара, вы не являетесь его владельцем.")

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


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("home")
    template_name = 'delete_product.html'

    def post(self, request, *args, **kwargs) -> Any:
        obj = Product.objects.get(id=kwargs['pk'])
        user = self.request.user
        if obj.owner != request.user and not is_moder(user):
            return HttpResponseForbidden(
                "У вас нет прав для удаления товара, вы не являетесь его владельцем или модератором")

        if not request.user.has_perm('catalog.delete_product'):
            return HttpResponseForbidden("У вас нет прав для удаления товара")

        super(ProductDeleteView, self).post(request, *args, **kwargs)

        return redirect('home')

    template_name = 'delete_product.html'


def send_letter(request) -> None:
    send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL])
    return render(request, "home.html")

@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryProductsListView(generic.ListView):
    model = Product
    template_name = "category_products.html"
    context_object_name = 'items'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        cat_id = self.kwargs.get('pk')
        if cat_id:
            cat = Category.objects.get(pk=cat_id)
            context['category'] = cat
        return context

    def get_queryset(self):

        cat_id = self.kwargs.get('pk')
        if cat_id:
            key_name = f"products_queryset_{cat_id}"
            queryset = cache.get(key_name)
            if not queryset:
                cat = Category.objects.get(pk=cat_id)
                if cat:
                    queryset = ProductService.products_of_category(cat_id)
                    cache.set(key_name, queryset, 60 * 15)
                else:
                    queryset = Product.objects.all()
            else:
                queryset = Product.objects.all()
        else:
            queryset = Product.objects.all()
        return queryset
