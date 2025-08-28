from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin, User
# Create your models here.
from django.core.validators import RegexValidator
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class User(AbstractUser, PermissionsMixin):
    is_store = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Store(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    slug = models.SlugField(unique=True, db_index=True)
    category = models.ManyToManyField(Category, related_name='products')
    seller = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    #images = models.ImageField(upload_to="product", null=True, upload_to='product_images/%Y/%m/')
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.user.username}, {self.product}, {self.quantity}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField(null=True)#for customer

    def __str__(self):
        formatted_date = self.date.strftime('%Y-%m-%d %H:%M')
        return f'{self.customer.user.username} {formatted_date} {self.pk}'


class Status(models.Model):
    name = models.CharField(max_length=20, default="Ordered")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Statuses'

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order.customer.user.username



