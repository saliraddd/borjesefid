from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Wallet, Transaction


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'phone_number', 
        'email', 
        'user_type', 
        'is_verified', 
        'wallet_balance', 
        'is_active', 
        'is_staff', 
        'date_joined'
    )
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('phone_number', 'email', 'national_id')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('اطلاعات شخصی', {
            'fields': (
                'email', 'user_type', 'national_id', 'address', 'city',
                'profile_picture', 'is_verified', 'agency_license', 'agency_commission_rate'
            )
        }),
        ('کیف پول', {'fields': ('wallet_balance',)}),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'email', 'password1', 'password2', 'user_type',
                'is_verified', 'is_active', 'is_staff'
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_charged', 'total_spent')
    list_filter = ('created_at',)
    search_fields = ('user__phone_number',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'wallet', 'get_user_phone', 'transaction_type', 
        'amount', 'status', 'created_at'
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('wallet__user__phone_number', 'reference_id')
    readonly_fields = ('created_at', 'updated_at')

    def get_user_phone(self, obj):
        return obj.wallet.user.phone_number
    get_user_phone.short_description = 'شماره موبایل کاربر'