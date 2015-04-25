# -*- coding: utf-8 -*-
from pagedown.widgets import AdminPagedownWidget
from django.db import models
from django.contrib import admin
from blog.models import Post, Tag
from sorl.thumbnail import default

ADMIN_THUMBS_SIZE = '100x100'


class TagAdmin(admin.ModelAdmin):
    def image_display(self, obj):
        if obj.poster:
            thumb = default.backend.get_thumbnail(obj.poster, ADMIN_THUMBS_SIZE)
            return '<img src="%s" width="%s" />' % (thumb.url, thumb.width)
        else:
            return 'No Image'
    image_display.allow_tags = True
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget(show_preview=False)},
    }
    fieldsets = (
        ('Content', {
            'fields': ('name', 'poster', 'content')
        }),
    )
    readonly_fields = ('slug',)
    list_display = ('name', 'image_display')
    list_per_page = 15


class PostAdmin(admin.ModelAdmin):
    def get_author_name(self, obj):
        return obj.author.name

    def image_display(self, obj):
        if obj.poster:
            thumb = default.backend.get_thumbnail(obj.poster, ADMIN_THUMBS_SIZE)
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
            'fields': ('slug', 'date', 'views')
        }),
        ('Content', {
            'fields': ('status', 'title', 'poster', 'content', 'tags')
        }),
    )
    list_editable = ('status',)
    readonly_fields = ('views', 'slug')
    list_display = ('title', 'image_display', 'date', 'get_author_name', 'status')
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
