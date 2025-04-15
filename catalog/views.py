from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        return render(request, 'response.html')
    else:
        return render(request, 'contacts.html')


def posted_info(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return render(request, 'response.html', context={'user_name': user_name,
                                                         'phone': phone, 'message': message})
    else:
        return render(request, 'contacts.html')
