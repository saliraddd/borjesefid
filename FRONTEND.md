# 🎫 FRONTEND - بُرج سفید

## 📁 ساختار فایل‌ها

```
templates/
├── base.html                 # صفحه پایه (Base Template)
├── home.html                 # صفحه اصلی
├── flight_list.html          # لیست پروازها
├── flight_detail.html        # جزئیات پرواز
├── create_booking.html       # فرم رزرو
├── booking_list.html         # لیست رزروهای کاربر
└── booking_detail.html       # جزئیات رزرو

static/
├── css/
│   └── style.css            # تمام استایل‌های اضافی
├── js/
│   └── main.js              # تمام اسکریپت‌های اضافی
└── images/                  # تصاویر و آیکون‌ها
```

---

## 🎨 ویژگی‌های Design

### رنگ‌ها
- **رنگ اصلی**: `#1e3c72` (آبی تیره)
- **رنگ دوم**: `#2a5298` (آبی روشن)
- **رنگ موفقیت**: `#27ae60` (سبز)
- **رنگ خطر**: `#e74c3c` (قرمز)
- **رنگ هشدار**: `#f39c12` (نارنجی)

### فونت‌ها
- فونت اصلی: `IRANSans` (فونت فارسی)
- فونت دوم: `Segoe UI`

---

## 📄 توضیح Templates

### 1. **base.html** - صفحه پایه
- Header با لوگو و ناویگیشن
- Main content area
- Footer
- Message display
- استایل‌های کلی

### 2. **home.html** - صفحه اصلی
- Hero section (بنر بزرگ)
- فرم جستجوی پروازها
- بخش ویژگی‌ها
- نمایش آخرین پروازها
- بخش آمار و اطلاعات
- CTA (Call To Action)

### 3. **flight_list.html** - لیست پروازها
- فیلترها (مبدأ، مقصد، تاریخ، قیمت)
- گزینه‌های مرتب‌سازی
- نمایش کارت پروازها
- اطلاعات پرواز (ساعت، ایرلاین، صندلی‌ها)
- دکمه رزرو

### 4. **flight_detail.html** - جزئیات پرواز
- خلاصه پرواز
- اطلاعات تفصیلی
- Timeline مسیر پرواز
- امکانات موجود
- فرم رزرو

### 5. **create_booking.html** - فرم رزرو
- خلاصه پرواز
- فرم اطلاعات مسافران
- فرم اطلاعات تماس
- محاسبه قیمت
- دکمه تایید و پرداخت

### 6. **booking_list.html** - لیست رزروها
- نمایش تمام رزروهای کاربر
- وضعیت رزرو
- دکمه‌های عملیات (مشاهده، لغو، چاپ)
- اطلاعات کد رزرو

---

## 🎯 CSS Classes و Utilities

### رنگ‌های متن
```css
.text-primary     /* رنگ اصلی */
.text-secondary   /* رنگ دوم */
.text-success     /* سبز */
.text-danger      /* قرمز */
.text-warning     /* نارنجی */
.text-muted       /* خاکستری */
```

### دکمه‌ها
```css
.btn              /* دکمه عادی */
.btn-primary      /* دکمه اصلی */
.btn-secondary    /* دکمه دوم */
.btn-success      /* دکمه موفقیت */
.btn-danger       /* دکمه خطر */
```

### کارت‌ها
```css
.card             /* کارت عادی */
.card-header      /* سر کارت */
.card-body        /* بدن کارت */
.card-footer      /* پایین کارت */
```

### فاصل‌ها
```css
.mt-10, .mt-20, .mt-30    /* Margin Top */
.mb-10, .mb-20, .mb-30    /* Margin Bottom */
.p-10, .p-20, .p-30       /* Padding */
```

### Grid
```css
.grid-2   /* 2 ستون */
.grid-3   /* 3 ستون */
.grid-4   /* 4 ستون */
```

---

## 📱 Responsive Design

تمام صفحات برای تمام دستگاه‌ها بهینه شده‌اند:
- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

---

## ⚙️ JavaScript Functions

### توابع اساسی

#### `smoothScroll(target)`
تغییر صفحه با انیمیشن
```javascript
bookingApp.smoothScroll('.search-box');
```

#### `formatCurrency(amount)`
فرمت‌کردن قیمت
```javascript
bookingApp.formatCurrency(1000000); // ۱,۰۰۰,۰۰۰ تومان
```

#### `showAlert(message, type)`
نمایش هشدار
```javascript
bookingApp.showAlert('رزرو شما موفق بود!', 'success');
```

#### `filterByPrice(minPrice, maxPrice)`
فیلتر کردن پروازها بر اساس قیمت
```javascript
bookingApp.filterByPrice(100000, 500000);
```

#### `getQueryParameter(param)`
دریافت پارامتر از URL
```javascript
const origin = bookingApp.getQueryParameter('origin');
```

---

## 🎨 Icon Library

استفاده از Font Awesome 6.4.0:
```html
<i class="fas fa-plane"></i>                <!-- هواپیما -->
<i class="fas fa-map-location-dot"></i>     <!-- مکان -->
<i class="fas fa-money-bill-wave"></i>      <!-- قیمت -->
<i class="fas fa-clock"></i>                <!-- ساعت -->
<i class="fas fa-search"></i>               <!-- جستجو -->
<i class="fas fa-check"></i>                <!-- تایید -->
<i class="fas fa-times"></i>                <!-- لغو -->
<i class="fas fa-info-circle"></i>          <!-- اطلاع -->
```

---

## 📚 نمونه کدهای مفید

### فیلتر پروازها
```html
<form method="GET" action="{% url 'flights:flight_list' %}">
    <input type="text" name="origin" placeholder="مبدأ">
    <input type="text" name="destination" placeholder="مقصد">
    <button type="submit">جستجو</button>
</form>
```

### نمایش پرواز
```html
<div class="flight-card">
    <div class="flight-left">
        <div class="flight-times">
            <div class="departure-time">{{ flight.departure_time|date:"H:i" }}</div>
        </div>
        <div class="flight-info">
            <div class="flight-route">{{ flight.origin_city }} → {{ flight.destination_city }}</div>
        </div>
    </div>
    <div class="flight-right">
        <div class="flight-price">{{ flight.price_per_seat|floatformat:"0" }} تومان</div>
        <button class="flight-btn">رزرو کنید</button>
    </div>
</div>
```

---

## 🚀 نکات مهم

1. **استفاده از `extends`**: تمام صفحات از `base.html` ارث می‌برند
2. **استفاده از `include`**: می‌توانید قطعات را جدا کنید
3. **CSRF Token**: تمام فرم‌ها باید `{% csrf_token %}` داشته باشند
4. **Template Tags**: از Django template tags استفاده کنید (`{% url %}`, `{% if %}`, etc.)
5. **مجموعه Static Files**: قبل از Deploy، `python manage.py collectstatic` اجرا کنید

---

## 📝 نمونه View برای صفحات

```python
from django.shortcuts import render, get_object_or_404
from flights.models import Flight

def flight_list(request):
    flights = Flight.objects.filter(status='active')
    return render(request, 'flight_list.html', {'flights': flights})

def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    return render(request, 'flight_detail.html', {'flight': flight})
```

---

## 🔧 بهبود‌های آینده

- [ ] اضافه کردن Animation‌های بیشتر
- [ ] بهتر کردن Mobile UI
- [ ] اضافه کردن Dark Mode
- [ ] بهینه‌سازی Performance
- [ ] اضافه کردن PWA Support
- [ ] بهبود Accessibility

---

**آخرین بروزرسانی**: 15 دسامبر 2025
