from django.contrib import admin
from profiles.models import Profile
from sorl.thumbnail import default

ADMIN_THUMBS_SIZE = '40x40'


class ProfileAdmin(admin.ModelAdmin):
    def image_display(self, obj):
        if obj.photo:
            thumb = default.backend.get_thumbnail(obj.photo, ADMIN_THUMBS_SIZE)
            return '<img src="%s" width="%s" />' % (thumb.url, thumb.width)
        else:
            return 'No Image'
    image_display.allow_tags = True
    fieldsets = (
        ('Content', {
            'fields': ('user', 'name', 'photo')
        }),
    )
    readonly_fields = ('slug',)
    list_display = ('name', 'image_display')
    list_per_page = 15

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
