# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={'placeholder': '0912xxxxxxx', 'dir': 'ltr'})
    )


class CustomerSignupForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={'placeholder': '0912xxxxxxx'})
    )
    email = forms.EmailField(required=False, label="ایمیل (اختیاری)")

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']
        user.user_type = 'customer'
        user.is_verified = False  # تا وقتی OTP تایید نشه
        if commit:
            user.save()
        return user


class AgencySignupForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=True, label="شماره موبایل")
    email = forms.EmailField(required=True, label="ایمیل")
    agency_name = forms.CharField(max_length=200, label="نام آژانس")
    agency_license = forms.FileField(label="مجوز فعالیت آژانس (PDF/JPG)", required=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email', 'agency_license'] #'agency_name',

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            phone_number=self.cleaned_data['phone_number'],
            email=self.cleaned_data['email'],
            password=None,  # بدون پسورد اولیه → بعداً با OTP ست می‌شه
            user_type='agency',
            is_verified=False,
        )
        # می‌تونی agency_name رو در یک مدل جدا (AgencyProfile) ذخیره کنی یا به فیلد اضافه کنی
        # فعلاً ساده: فقط لایسنس ذخیره می‌کنیم
        user.agency_license = self.cleaned_data['agency_license']
        if commit:
            user.save()
        return user