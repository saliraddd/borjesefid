from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import LoginForm, CustomerSignupForm, AgencySignupForm
from .models import CustomUser
import random
# from django.core.mail import send_mail  # اگر بعداً نیاز داشتی

def send_otp(request, phone, email=None):
    """تولید و ارسال OTP - فعلاً فقط چاپ + ذخیره در session"""
    otp = random.randint(100000, 999999)
    request.session['otp'] = otp
    request.session['otp_created_at'] = str(int(random.random() * 1000000))  # برای expire ساده

    print(f"OTP برای {phone}: {otp}")  # ← تست

    # اگر ایمیل داری بعداً اینجا فعال کن
    # if email:
    #     send_mail(
    #         'کد تایید بورج سفید',
    #         f'کد شما: {otp}\n\nاین کد ۳ دقیقه اعتبار دارد.',
    #         'noreply@borjesefid.com',
    #         [email],
    #     )

    return otp


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number'].strip()
            try:
                user = CustomUser.objects.get(phone_number=phone)
                send_otp(request, phone, user.email)
                request.session['auth_phone'] = phone
                request.session['auth_mode'] = 'login'
                return redirect('accounts:verify_otp')
            except CustomUser.DoesNotExist:
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'error': 'این شماره موبایل ثبت‌نام نشده است.'
                })
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def verify_otp(request):
    entered_otp = request.POST.get('otp', '').strip()
    session_otp = request.session.get('otp')
    phone = request.session.get('auth_phone')

    if not phone or not session_otp:
        return render(request, 'accounts/verify_otp.html', {'error': 'اطلاعات جلسه منقضی شده است.'})

    if entered_otp == str(session_otp):
        try:
            user = CustomUser.objects.get(phone_number=phone)
            user.is_verified = True
            user.save(update_fields=['is_verified'])

            login(request, user)

            # پاک کردن اطلاعات موقتی
            keys_to_remove = ['otp', 'auth_phone', 'auth_mode', 'signup_phone']
            for key in keys_to_remove:
                request.session.pop(key, None)

            return redirect('flights:home')   # یا 'accounts:dashboard'
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'کاربر یافت نشد'}, status=400)
    else:
        return render(request, 'accounts/verify_otp.html', {
            'error': 'کد وارد شده اشتباه است.',
            'phone': phone
        })


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_otp(request, user.phone_number, user.email)
            request.session['auth_phone'] = user.phone_number
            request.session['auth_mode'] = 'signup'
            return redirect('accounts:verify_otp')
    else:
        form = CustomerSignupForm()

    return render(request, 'accounts/signup_customer.html', {'form': form})


def agency_signup(request):
    if request.method == 'POST':
        form = AgencySignupForm(request.POST, request.FILES)
        if form.is_valid():
            phone = form.cleaned_data['phone_number'].strip()
            email = form.cleaned_data['email'].strip()

            if CustomUser.objects.filter(phone_number=phone).exists():
                form.add_error('phone_number', 'این شماره قبلاً ثبت شده است.')
            else:
                user = CustomUser.objects.create_user(
                    phone_number=phone,
                    email=email,
                    password=None,          # بعداً می‌تونی ست کنی یا بدون پسورد بمونه
                    user_type='agency',
                    is_verified=False,
                )
                user.agency_license = form.cleaned_data['agency_license']
                # اگر بعداً agency_name رو به مدل اضافه کردی:
                # user.agency_name = form.cleaned_data['agency_name']
                user.save()

                send_otp(request, phone, email)
                request.session['auth_phone'] = phone
                request.session['auth_mode'] = 'signup_agency'
                return redirect('accounts:verify_otp')
    else:
        form = AgencySignupForm()

    return render(request, 'accounts/signup_agency.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('flights:home')