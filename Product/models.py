from django.db import models
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey('Vendor.Vendor', on_delete=models.CASCADE)

    def __str__(self):
        return self.name