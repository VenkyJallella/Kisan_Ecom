from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'home.html')


def contact_us(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Message sent Successufully!')
            return redirect('contact_us')
        
            
    return render(request, 'contact.html', {'form':form})

