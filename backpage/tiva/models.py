from django.db import models
from django.contrib.auth.models import User

class Coats(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='coats/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Coats"

    def __str__(self):
        return self.title


class Shirts(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shirts/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Shirts"

    def __str__(self):
        return self.title


class Pants(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pants/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Pants"

    def __str__(self):
        return self.title


class Tshirt(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tshirts/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Tshirt"

    def __str__(self):
        return self.title


class Watches(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='watches/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Watches"

    def __str__(self):
        return self.title


class Perfumes(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='perfumes/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Perfumes"

    def __str__(self):
        return self.title


class Shoes(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shoes/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Shoes"

    def __str__(self):
        return self.title

class Sandals(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sandals/',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sandals"

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=500,blank=True, null=True)
    quantity = models.IntegerField(default=1)
    @property
    def total_price(self):
       return self.price * self.quantity
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.full_name
class Review(models.Model):
    CATEGORY_CHOICES = [
        ("coats", "Coats"),
        ("shirts", "Shirts"),
        ("pants", "Pants"),
        ("tshirt", "Tshirt"),
        ("watches", "Watches"),
        ("perfumes", "Perfumes"),
        ("shoes", "Shoes"),
        ("sandals", "Sandals"),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    product_id = models.IntegerField()

    user_name = models.CharField(max_length=100)

    rating = models.IntegerField(
        choices=[
            (1, "⭐"),
            (2, "⭐⭐"),
            (3, "⭐⭐⭐"),
            (4, "⭐⭐⭐⭐"),
            (5, "⭐⭐⭐⭐⭐"),
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user_name} - {self.rating}★"