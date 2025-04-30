import os.path
from http.client import HTTPResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.views import generic
from django.core.paginator import Paginator

from config.settings import BASE_DIR
from .models import ContactsInfo, Product, Category
from typing import Any


# class ProductDetailView(generic.DetailView):
#     model = Product
#     template_name = "product_details.html"


def home(request) -> HTTPResponse | Any:
    latest_products = Product.objects.all().order_by("-created_at")       # [:5]

    paginator = Paginator(latest_products, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})

    # return render(request, "home.html", context={"items": latest_products})


def contacts(request) -> HTTPResponse | Any:
    if request.method == "POST":
        return render(request, "response.html")
    else:
        try:
            contacts = ContactsInfo.objects.order_by("-updated_at")[0]
        except:
            contacts = None
        return render(request, "contacts.html", context={"contacts": contacts})


def new_category(request) -> HTTPResponse | Any:
    return render(request, "new_category.html")


def add_category(request) -> HTTPResponse | Any:
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_desc = request.POST.get("category_desc")
        error_code = 0
        error_message = ''
        if category_name:
            same_name_cats = Category.objects.filter(name=category_name)
            if same_name_cats.exists():
                error_code = 1
            else:
                try:
                    new_cat = Category.objects.create(name=category_name, description=category_desc)
                    new_cat.save()
                except Exception as e:
                    error_code = 3
                    error_message = str(e)
        else:
            error_code = 2

        if error_code:
            error_data = {'error_code': error_code, 'error_message': error_message}
            return render(request, "creation_error.html", context=error_data)
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, "new_category.html")


def new_product(request) -> HTTPResponse | Any:
    categories = Category.objects.all().order_by('name')
    return render(request, "new_product.html", context={'categories': categories})

def add_product(request) -> HTTPResponse | Any:
    if request.method == "POST":
        error_code = 0
        error_message = ''

        product_name = request.POST.get("product_name")
        if product_name:
            same_name_prods = Product.objects.filter(name=product_name)
            if same_name_prods.exists():
                error_code = 100  # product already exists
            else:
                product_price = request.POST.get("product_price")

                if product_price:
                    try:
                        product_price = float(product_price)
                    except:
                        error_code = 102  # no product price

                    if product_price > 0.0:
                        category_name = request.POST.get("category_name")

                        if category_name:
                            try:
                                category = Category.objects.get(name=category_name)
                            except Category.DoesNotExist:
                                error_code = 104  # nonexistent category
                            else:
                                file_name = ''
                                if 'image_file' in request.FILES:
                                    file = request.FILES['image_file']

                                    images_storage = FileSystemStorage(
                                        location=os.path.join(BASE_DIR, 'catalog', 'static', 'images'))
                                    file_name = str(file.name).strip().replace(' ','_')
                                    import re
                                    file_name = re.sub(r'[ЁёА-я]', '', file_name)
                                    images_storage.save(file_name, content=ContentFile(file.read()))

                                product_desc = request.POST.get("product_desc")
                                    # print(f"product_name: {product_name} type: {type(product_name)}")
                                    # print(f"product_price: {product_price} type: {type(product_price)}")
                                    # print(f"category: {category} type: {type(category)}")
                                    # print(f"image_file: {image_file} type: {type(image_file)}")
                                try:
                                    new_product_obj = Product.objects.create(name=product_name,
                                                                             description=product_desc,
                                                                             price=product_price, category=category,
                                                                             image=request.FILES.get("image_file"))
                                    new_product_obj.save()
                                except Exception as e:
                                    error_code = 105  # creation failed
                                    error_message = str(e)
                        else:
                            error_code = 103  # no product category
                    else:
                        error_code = 106  # zero price
        else:
            error_code = 101  # no product name

        if error_code:
            error_data = {'error_code': error_code, 'error_message': error_message}
            return render(request, "creation_error.html", context=error_data)
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, "new_product.html")


def details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product_details.html", context={"product": product})


def posted_info(request) -> HTTPResponse | Any:
    if request.method == "POST":
        user_name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return render(
            request,
            "response.html",
            context={"user_name": user_name, "phone": phone, "message": message},
        )
    else:
        return render(request, "contacts.html")
