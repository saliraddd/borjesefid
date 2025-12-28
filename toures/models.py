from django.db import models
from django.urls import reverse

class Tour(models.Model):
    TOUR_TYPE_CHOICES = [
        ('internal', 'داخلی'),
        ('external', 'خارجی'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان تور")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ (برای URL)")
    destination = models.CharField(max_length=100, verbose_name="مقصد")
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPE_CHOICES, verbose_name="نوع تور")
    duration = models.PositiveIntegerField(verbose_name="مدت تور (روز)")
    departure_date = models.DateField(verbose_name="تاریخ رفت")
    return_date = models.DateField(verbose_name="تاریخ برگشت", blank=True, null=True)
    price_per_person = models.PositiveBigIntegerField(verbose_name="قیمت به ریال (هر نفر)")
    available_seats = models.PositiveIntegerField(verbose_name="ظرفیت موجود")
    description = models.TextField(verbose_name="توضیحات تور")
    image = models.ImageField(upload_to='tours/', verbose_name="تصویر اصلی تور", blank=True, null=True)
    featured = models.BooleanField(default=False, verbose_name="تور ویژه (نمایش در صفحه اصلی)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ['-departure_date']
        verbose_name = "تور"
        verbose_name_plural = "تورها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('toures:tour_detail', args=[self.slug])

