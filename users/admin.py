from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.

User = get_user_model()


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email',)
    list_filter = ('email', 'phone_number', 'is_active',)
    ordering = ('-full_name',)
    list_display = ('__str__', 'email', 'is_active', 'phone_number')
    fieldsets = (
        (None, {'fields': (
            'email',
            'phone_number',
            'password',
            'full_name',
            )}),
        ('Permissions',
         {
             'fields': (
                 'is_active',
                 'is_staff',
                 'is_superuser',
                 'verified',
                 'groups',
                 'user_permissions'
             )
         }),
    )

    # fieldsets to add a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone_number',
                'full_name',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'groups',
                'user_permissions'
                )}
         ),
    )


admin.site.register(User, UserAdminConfig)

from .models import Otp
admin.site.register(Otp)