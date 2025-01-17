from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




# Create your models here.
status = (
    ("ACTIVE","1"),
    ("INACTIVE","0")
)

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        value = timezone.now()
        setattr(model_instance, self.attname, value)
        return timezone.now()

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number','username']

    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=13,null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=155,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username

class Product(models.Model):
    name = models.CharField(max_length=20,null=True,blank=True)
    prodcut_category = models.CharField(max_length=20,null=True,blank=True)
    price = models.IntegerField()
    files = models.ImageField(upload_to='images/')
    status = models.BooleanField(default = False)
    updation = AutoDateTimeField(default=timezone.now)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    tottal_price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default = True)

    def __str__(self):
        if self.user_id:
            return self.user_id.name


class Order(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    # address = models.CharField(max_length=100,null=True,blank=True)
    is_paid = models.BooleanField()
    total_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    order_status =models.BooleanField(default =True)


    def __str__(self):
        if self.user_id:
            return self.user_id.name
