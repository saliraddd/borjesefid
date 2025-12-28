from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Wallet, Transaction
from bookings.models import Booking

@login_required(login_url='accounts:login')
def dashboard(request):
    """صفحه‌ی پیش‌خوان کاربر"""
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)
    
    # آخرین تراکنش‌ها
    transactions = wallet.transactions.all().order_by('-created_at')[:10]
    
    # رزروهای کاربر
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'wallet': wallet,
        'transactions': transactions,
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'page': 'dashboard'
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def dashboard_transactions(request):
    """لیست تراکنش‌های کاربر"""
    try:
        wallet = Wallet.objects.get(user=request.user)
        transactions = wallet.transactions.all().order_by('-created_at')
    except Wallet.DoesNotExist:
        transactions = []
    
    context = {
        'transactions': transactions,
        'page': 'transactions',
        'wallet': wallet if wallet else None
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def dashboard_bookings(request):
    """لیست رزروهای کاربر"""
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'bookings': bookings,
        'page': 'bookings',
        'wallet': None
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def dashboard_profile(request):
    """مشخصات کاربر"""
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)
    
    context = {
        'wallet': wallet,
        'page': 'profile'
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def charge_credit(request):
    """صفحه‌ی شارژ اعتبار"""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            wallet = Wallet.objects.get(user=request.user)
            amount = int(amount)
            
            # ایجاد تراکنش
            transaction = Transaction.objects.create(
                wallet=wallet,
                transaction_type='charge',
                amount=amount,
                status='pending',
                description='شارژ اعتبار از طریق پرداخت آنلاین'
            )
            
            # TODO: اتصال به درگاه پرداخت (زرین‌پال، بانک‌ملی و...)
            return redirect('accounts:payment_gateway', transaction_id=transaction.id)
        except:
            pass
    
    context = {'page': 'charge'}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def withdrawal_request(request):
    """درخواست برداشت اعتبار"""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        bank_account = request.POST.get('bank_account')
        
        try:
            wallet = Wallet.objects.get(user=request.user)
            amount = int(amount)
            
            if amount <= wallet.balance:
                # ایجاد درخواست برداشت
                transaction = Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='withdrawal',
                    amount=amount,
                    status='pending',
                    description=f'درخواست برداشت به حساب {bank_account}'
                )
                return redirect('accounts:dashboard')
        except:
            pass
    
    try:
        wallet = Wallet.objects.get(user=request.user)
    except:
        wallet = None
    
    context = {
        'wallet': wallet,
        'page': 'withdrawal'
    }
    return render(request, 'accounts/dashboard.html', context)
