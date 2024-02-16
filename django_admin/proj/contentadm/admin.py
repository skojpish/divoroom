from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models

class DisplayFeedback(admin.ModelAdmin):
    list_display = ['number', 'feedback_photo']

    def feedback_photo(self, object):
        if object.review_ph:
            return mark_safe(f"<img src='{object.review_ph.url}' width=200>")

    feedback_photo.short_description = "Отзыв"

    def number(self, obj):
        queryset = self.model.objects.all()

        return list(queryset).index(obj) + 1

    number.short_description = '№'

admin.site.register(models.Feedback, DisplayFeedback)
