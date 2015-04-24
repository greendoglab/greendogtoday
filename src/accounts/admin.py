""" Admin definition for EmailUser."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):

    """EmailUser Admin model."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (None, {'fields': (
            'name', 'photo', 'poster',
            'twitter', 'instagram', 'facebook',
            'google', 'website', 'content',
            'slug'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
    ),
    )

    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register the new EmailUserAdmin
admin.site.register(Account, AccountAdmin)
