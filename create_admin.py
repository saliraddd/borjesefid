from django.contrib.auth.models import User

# ادمین قبلی را حذف کنید اگر وجود دارد
User.objects.filter(username='admin').delete()

# ادمین جدید ایجاد کنید
User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
print("✅ Admin user created: admin / admin123")
