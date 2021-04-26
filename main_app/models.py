from django.db import models

# Import the reverse function
from django.urls import reverse

class Feelings(models.Model):
    status = models.CharField(max_length=10)
    color = models.CharField(max_length=20)

    # Other goodness such as 'def __str__():' below
    def __str__(self):
        return f'{self.status} {self.color}'

    # Add this method
    def get_absolute_url(self):
        return reverse('feelings_detail', kwargs={'feelings_id': self.id})    

# Create your models here.
class Crypto(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    amount = models.IntegerField()

    # Add the M:M relationship
    feelings = models.ManyToManyField(Feelings)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'crypto_id': self.id})


# purchase model
class Purchase(models.Model):
    date = models.DateField('Purchase Date')
    purchase_price = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    # Create a crypto_id FK
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_purchase_display()} on {self.date}"

    # change the default sort
    class Meta:
        ordering = ['-date']

# photo model
class Photo(models.Model):
    url = models.CharField(max_length=200)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for crypto_id: {self.crypto_id} @{self.url}"