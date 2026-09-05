from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    manager_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    users = models.ManyToManyField(User, related_name='stores', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=50, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    lead_time_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    max_stock_level = models.IntegerField(default=100)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'product')

    def __str__(self):
        return f"{self.product.name} at {self.store.name}: {self.quantity}"


class SalesTransaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('other', 'Other')
    ], default='cash')

    def __str__(self):
        return f"{self.product.name} x {self.quantity} at {self.store.name} on {self.transaction_date.date()}"


class InventoryAlert(models.Model):
    ALERT_TYPES = [
        ('stock_out', 'Stock Out'),
        ('low_stock', 'Low Stock'),
        ('overstock', 'Overstock'),
        ('slow_moving', 'Slow Moving'),
        ('sales_spike', 'Sales Spike'),
        ('sales_drop', 'Sales Drop'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='alerts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    message = models.TextField()
    recommended_action = models.TextField()
    data_snapshot = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert_type} - {self.product.name} at {self.store.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    default_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
