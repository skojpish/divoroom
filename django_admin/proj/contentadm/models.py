from django.db import models

class Feedback(models.Model):
    review_ph = models.ImageField(verbose_name="Отзыв", upload_to="feedback/")
    image_id = models.CharField(verbose_name="image ID", blank=True, null=True, editable=False)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'