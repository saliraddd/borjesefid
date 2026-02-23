from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره موبایل الزامی است')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('customer', 'مشتری عادی'),
        ('agency', 'کاربر آژانسی'),
        ('staff', 'کارمند/مدیر'),
    ]

    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="شماره موبایل معتبر نیست.")],
        unique=True
    )
    first_name = models.CharField("نام", max_length=150, blank=True)
    last_name  = models.CharField("نام خانوادگی", max_length=150, blank=True)
    email = models.EmailField(blank=True, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    national_id = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    agency_license = models.FileField(upload_to='agency_documents/', blank=True, null=True)
    agency_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']  # برای superuser

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        if self.first_name:
            return self.first_name.strip()
        if self.email:
            return self.email.split('@')[0]
        return self.phone_number   # fallback نهایی

    def get_short_name(self):
        return self.display_name

    def get_full_name(self):
        return self.display_name

    def __str__(self):
        return self.phone_number


class Wallet(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    total_charged = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    total_spent = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"کیف پول {self.user.username} - {self.balance} تومان"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('charge', 'شارژ'),
        ('withdrawal', 'برداشت'),
        ('booking', 'خرید بلیط'),
        ('refund', 'بازپرداخت'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'انجام‌شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو‌شده'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    description = models.TextField(blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} تومان - {self.get_status_display()}"


