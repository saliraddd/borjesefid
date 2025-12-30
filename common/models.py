from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام شهر")
    name_en = models.CharField(max_length=100, verbose_name="نام انگلیسی")
    iata_code = models.CharField(max_length=3, unique=True, verbose_name="کد IATA")
    country = models.CharField(max_length=100, verbose_name="کشور")
    is_popular = models.BooleanField(default=False, verbose_name="شهر محبوب")

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.iata_code})"


class Airline(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام ایرلاین")
    name_en = models.CharField(max_length=100, verbose_name="نام انگلیسی")
    iata_code = models.CharField(max_length=2, unique=True, verbose_name="کد IATA")  # مثل IR, EP
    logo = models.ImageField(upload_to='airlines/', blank=True, null=True, verbose_name="لوگو")

    class Meta:
        verbose_name = "ایرلاین"
        verbose_name_plural = "ایرلاین‌ها"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.iata_code})"