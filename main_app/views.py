from django.shortcuts import render

from django.http import HttpResponse


class Crypto:  
    def __init__(self, name, price, description, amount):
        self.name = name
        self.price = price
        self.description = description
        self.amount = amount

cryptos = [
  Crypto('Bitcoin', 60000, 'OG bitty', 3),
  Crypto('Litecoin', 300, 'fork of bitty but is litty', 500),
]

# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cryptos_index(request):
    return render(request, 'cryptos/index.html', { 'cryptos': cryptos })