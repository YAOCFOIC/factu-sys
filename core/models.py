from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    mfa_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Client(models.Model):
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=20)
    address = models.TextField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('rechazada', 'Rechazada'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    cufe = models.CharField(max_length=100, unique=True)

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class Backup(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='backups/')
    responsible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Report(models.Model):
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    pdf = models.FileField(upload_to='reports/')
    digital_signature = models.BooleanField(default=False)

class TaxValidation(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    response_message = models.TextField()
    validation_date = models.DateTimeField(auto_now_add=True)

class XMLUbl(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    content = models.TextField()
    sent_to_dian = models.BooleanField(default=False)