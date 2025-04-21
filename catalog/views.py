from django.shortcuts import render
from .models import Product, ContactsInfo


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', context={'items': latest_products})


def contacts(request):
    if request.method == 'POST':
        return render(request, 'response.html')
    else:
        contacts = ContactsInfo.objects.order_by('-updated_at')[0]
        return render(request, 'contacts.html', context={'contacts': contacts})


def posted_info(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return render(request, 'response.html', context={'user_name': user_name,
                                                         'phone': phone, 'message': message})
    else:
        return render(request, 'contacts.html')
