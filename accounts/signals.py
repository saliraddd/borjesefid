from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    """خودکار ایجاد کیف پول برای کاربر جدید"""
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    """ذخیره کیف پول کاربر"""
    if hasattr(instance, 'wallet'):
        instance.wallet.save()
