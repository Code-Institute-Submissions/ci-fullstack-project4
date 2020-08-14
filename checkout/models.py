from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Purchase(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.product_id} by"
        f" {self.user_id} on {self.purchase_date}"
