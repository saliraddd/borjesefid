from django.contrib import admin
from .models import City, Airline

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'iata_code', 'country', 'is_popular']
    list_filter = ['country', 'is_popular']
    search_fields = ['name', 'name_en', 'iata_code', 'country']
    list_editable = ['is_popular']
    ordering = ['name']
    fieldsets = (
        (None, {
            'fields': ('name', 'name_en', 'iata_code', 'country')
        }),
        ('تنظیمات پیشرفته', {
            'fields': ('is_popular',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'iata_code', 'display_logo']  # اسم متد نمایش رو تغییر دادم
    search_fields = ['name', 'name_en', 'iata_code']
    list_filter = ['name']
    fields = ('name', 'name_en', 'iata_code', 'logo')  # <-- logo رو به fields اضافه کن
    readonly_fields = ['display_logo']  # فقط نمایش تصویر قبلی readonly باشه

    def display_logo(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="150" height="80" style="object-fit: contain; border-radius: 8px;">'
        return "بدون لوگو"
    display_logo.allow_tags = True
    display_logo.short_description = "پیش‌نمایش لوگو"