from django.shortcuts import render, redirect

from django.http import HttpResponse

# import class-based-views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# import models
from .models import Crypto, Feelings, Photo
from .forms import PurchaseForm

# imports for image upload
import uuid
import boto3


# s3 variables
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'crypto-collector'
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

    # Get the feelings for crypto doesn't have
    feelings_crypto_doesnt_have = Feelings.objects.exclude(id__in = crypto.feelings.all().values_list('id'))

    # instantiate FeedingForm to be rendered in the template
    purchase_form = PurchaseForm()
    return render(request, 'cryptos/detail.html', { 
        'crypto': crypto, 
        'purchase_form':purchase_form,
        # Add the feelings to be displayed
        'feelings': feelings_crypto_doesnt_have
        })

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

# Feelings views
def feelings_index(request):
    feelings = Feelings.objects.all()
    context = {'feelings': feelings}
    
    return render(request, 'feeling/index.html', context)


def feeling_detail(request, feeling_id):
    feeling = Feelings.objects.get(id=feeling_id)
    context = {
        'feeling': feeling
    }
    return render(request, 'feeling/detail.html', context)
    
class Create_feeling(CreateView):
    model = Feelings
    fields = '__all__'


class Update_feeling(UpdateView):
    model = Feelings
    fields = ['color']

class Delete_feeling(DeleteView):
    model = Feelings
    success_url = '/feelings/' 

def assoc_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.add(feeling_id)
    return redirect('detail', crypto_id=crypto_id)

def remove_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.remove(feeling_id)
    return redirect('detail', crypto_id=crypto_id)

def add_photo(request, crypto_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to crypto_id or crypto (if you have a crypto object)
            photo = Photo(url=url, crypto_id=crypto_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', crypto_id=crypto_id)