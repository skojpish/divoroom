from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

class DisplayAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_html_photo1', 'get_html_photo2', 'get_html_photo3', 'price', 'description']
    list_edit = ['name', 'photo1', 'photo2', 'photo3', 'price', 'description']

    def get_html_photo1(self, object):
        if object.photo1:
            return mark_safe(f"<img src='{object.photo1.url}' width=50>")

    def get_html_photo2(self, object):
        if object.photo2:
            return mark_safe(f"<img src='{object.photo2.url}' width=50>")

    def get_html_photo3(self, object):
        if object.photo3:
            return mark_safe(f"<img src='{object.photo3.url}' width=50>")

    get_html_photo1.short_description = "Лицевое фото"
    get_html_photo2.short_description = "Доп. фото №1"
    get_html_photo3.short_description = "Доп. фото №2"



admin.site.register(models.Photo, DisplayAdmin)
