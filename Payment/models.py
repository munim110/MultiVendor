from django.db import models
from Product.models import OrderItem, Product
from django.contrib.auth.models import User

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('CANCELLED', 'CANCELLED')
)

# class payment(models.Model):
#     transaction_id = models.UUIDField()
#     validation_id = models.CharField(max_length=100)
#     amount = models.FloatField(decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.payment_id

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.UUIDField()
    amount = models.FloatField()
    products = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=100)
    # payment_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)