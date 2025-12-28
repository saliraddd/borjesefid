# ✅ خلاصه پروژه Django - سایت رزرو پرواز

## 🎯 آنچه انجام شد:

### 1️⃣ **ایجاد اپ‌های جدید:**
- ✅ `bookings` - مدیریت رزروها
- ✅ `payments` - مدیریت پرداخت‌ها
- ✅ `accounts` - مدیریت کاربران و پروفایل‌ها

### 2️⃣ **مدل‌های ایجاد شده:**

#### Flights App
```
Flight
├── flight_number (شماره پرواز)
├── airline (نام هواپیمایی)
├── origin_city → destination_city
├── departure_time → arrival_time
├── aircraft_type (نوع هواپیما)
├── total_seats → available_seats
├── price_per_seat (قیمت بلیط)
└── status (فعال/لغو شده)
```

#### Passengers App
```
Passenger
├── user (ForeignKey)
├── first_name / last_name
├── national_id (کد ملی)
├── passport_number (شماره پاسپورت)
└── date_of_birth (تاریخ تولد)
```

#### Bookings App
```
Booking
├── booking_code (کد رزرو)
├── user (ForeignKey - کاربری که رزرو کرده)
├── flight (ForeignKey - پرواز)
├── booking_date
├── status (در انتظار/تایید شده/لغو)
└── total_price

BookingPassenger (جدول ربط)
├── booking (ForeignKey)
├── passenger (ForeignKey)
└── seat_number (شماره صندلی)
```

#### Payments App
```
Payment
├── booking (OneToOneField)
├── amount (مبلغ)
├── payment_method (کارت/انتقال/کیف پول)
├── payment_date
├── status (در انتظار/موفق/ناموفق/بازگرداندی)
└── transaction_id
```

#### Accounts App
```
UserProfile
├── user (OneToOneField)
├── phone_number
├── national_id
├── address
├── city
├── profile_picture (تصویر)
└── is_verified (تایید شده)
```

### 3️⃣ **Views و URLs:**

#### Flights
- `GET /flights/` - لیست پروازها + جستجو
- `GET /flights/<id>/` - جزئیات پرواز

#### Bookings
- `GET /bookings/` - لیست رزروهای کاربر
- `GET /bookings/<id>/` - جزئیات رزرو
- `POST /bookings/create/<flight_id>/` - ایجاد رزرو

### 4️⃣ **مایگریشن‌ها:**
✅ تمام مایگریشن‌ها اعمال شدند

### 5️⃣ **Admin Panel:**
✅ تمام مدل‌ها در پنل ادمین ثبت شدند

---

## 📊 ساختار فایل‌ها:

```
d:\projects\django/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── create_sample_data.py
│
├── borj_sefid/
│   ├── settings.py (✅ اپ‌ها اضافه شدند)
│   ├── urls.py (✅ URLs اضافه شدند)
│   ├── asgi.py
│   └── wsgi.py
│
├── flights/
│   ├── models.py (✅ Flight مدل)
│   ├── views.py (✅ FlightListView, FlightDetailView)
│   ├── urls.py (✅ URLs)
│   ├── admin.py (✅ FlightAdmin)
│   └── migrations/
│
├── passengers/
│   ├── models.py (✅ Passenger مدل)
│   ├── admin.py (✅ PassengerAdmin)
│   └── migrations/
│
├── bookings/
│   ├── models.py (✅ Booking, BookingPassenger)
│   ├── views.py (✅ Views برای رزرو)
│   ├── urls.py (✅ URLs)
│   ├── admin.py (✅ BookingAdmin)
│   └── migrations/
│
├── payments/
│   ├── models.py (✅ Payment مدل)
│   ├── admin.py (✅ PaymentAdmin)
│   └── migrations/
│
└── accounts/
    ├── models.py (✅ UserProfile مدل)
    ├── admin.py (✅ UserProfileAdmin)
    └── migrations/
```

---

## 🔑 داده‌های لاگین:

**صورت حساب ادمین:**
- Username: `admin`
- Email: `admin@test.com`
- Password: `admin123`

**دسترسی:** http://localhost:8000/admin/

---

## 🚀 راه‌اندازی سرور:

```bash
# فعال کردن virtual environment
.venv\Scripts\activate

# اجرای سرور
python manage.py runserver

# سرور در آدرس زیر در دسترس است:
http://localhost:8000/
```

---

## 📋 مراحل بعدی (برای توسعه بیشتر):

1. ایجاد Template‌های HTML
   - flights/flight_list.html
   - flights/flight_detail.html
   - bookings/booking_list.html
   - bookings/booking_detail.html
   - bookings/create_booking.html

2. اضافه کردن Authentication Views
   - Register
   - Login
   - Logout

3. اضافه کردن Payment Gateway

4. ایجاد API (اختیاری - برای فرانت‌اند جدا)

5. تنظیمات امنیتی برای Production

---

## 🎨 ویژگی‌های پیادی شده:

- ✅ مدیریت پروازها
- ✅ مدیریت مسافران
- ✅ سیستم رزرو
- ✅ مدیریت پرداخت‌ها
- ✅ پروفایل کاربر
- ✅ جستجو در پروازها
- ✅ کنترل دسترسی (رزروهای فردی)
- ✅ Admin Panel
- ✅ محلی سازی (فارسی + منطقه‌زمانی تهران)

---

**ساخته شده با ❤️ با Django 6.0**
