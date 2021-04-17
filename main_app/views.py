from django.shortcuts import render, redirect

from django.http import HttpResponse

# import class-based-views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# import models
from .models import Crypto
from .forms import PurchaseForm

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
    # instantiate FeedingForm to be rendered in the template
    purchase_form = PurchaseForm()
    return render(request, 'cryptos/detail.html', { 'crypto': crypto, 'purchase_form':purchase_form })

def add_purchase(request, crypto_id):
    # create the ModelForm using the data in request.POST
    form = PurchaseForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the crypto_id assigned
        new_purchase = form.save(commit=False)
        new_purchase.crypto_id = crypto_id
        new_purchase.save()
    return redirect('detail', crypto_id=crypto_id)

class CryptoCreate(CreateView):
    model = Crypto
    fields = '__all__'

class CryptoUpdate(UpdateView):
    model = Crypto
    fields = ['price', 'description', 'amount']

class CryptoDelete(DeleteView):
    model = Crypto
    success_url = '/cryptos/'