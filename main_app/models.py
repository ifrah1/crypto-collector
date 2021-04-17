from django.db import models

# Import the reverse function
from django.urls import reverse

# Create your models here.
class Crypto(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    amount = models.IntegerField()

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