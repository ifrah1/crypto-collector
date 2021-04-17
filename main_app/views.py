from django.shortcuts import render

from django.http import HttpResponse

from .models import Crypto


# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cryptos_index(request):
    cryptos = Crypto.objects.all()
    return render(request, 'cryptos/index.html', { 'cryptos': cryptos })

def cryptos_detail(request, crypto_id):
    crypto = Crypto.objects.get(id=crypto_id)
    return render(request, 'cryptos/detail.html', { 'crypto': crypto })