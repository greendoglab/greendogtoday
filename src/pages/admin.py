# -*- coding: utf-8 -*-
from pagedown.widgets import AdminPagedownWidget
from django.db import models
from django.contrib import admin
from pages.models import Page
from sorl.thumbnail import default

ADMIN_THUMBS_SIZE = '100x100'


class PageAdmin(admin.ModelAdmin):
    def image_display(self, obj):
        if obj.poster:
            thumb = default.backend.get_thumbnail(
                obj.poster, ADMIN_THUMBS_SIZE
            )
            return '<img src="%s" width="%s" />' % (thumb.url, thumb.width)
        else:
            return 'No Image'
    image_display.allow_tags = True
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget(show_preview=False)},
    }
    fieldsets = (
        ('Additionally', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
        ('Content', {
            'fields': ('status', 'in_menu', 'title', 'poster', 'content')
        }),
    )
    list_display = ('title', 'image_display', 'status')
    readonly_fields = ('slug',)
    list_per_page = 15

admin.site.register(Page, PageAdmin)
