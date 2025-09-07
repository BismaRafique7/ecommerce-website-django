from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#class Category(models.Model):
 #   name = models.CharField(max_length=100)
   
  #  def __str__(self):
  #      return self.name
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    SIZES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    available_sizes = models.ManyToManyField("Size", blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_start = models.DateField(null=True, blank=True)
    sale_end = models.DateField(null=True, blank=True)
    shipping_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    stock = models.IntegerField(default=0)
    @property
    def on_sale(self):
        today = timezone.now().date()
        return self.sale_price and self.sale_start and self.sale_end and self.sale_start <= today <= self.sale_end

    def get_price(self):
        return self.sale_price if self.on_sale else self.price

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

class Size(models.Model):
    size = models.CharField(max_length=5)  # S, M, L

    def __str__(self):
        return self.size

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    name = models.CharField(max_length=100, null=True, blank=True)   # ✅ updated
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price at order time

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

