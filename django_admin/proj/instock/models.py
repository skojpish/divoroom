from django.db import models

class Photo(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=50, null=True)
    photo1 = models.ImageField(verbose_name="Добавить лиц. фото", upload_to="in_stock/", blank=True)
    photo2 = models.ImageField(verbose_name="Добавить доп. фото №1", upload_to="in_stock/", blank=True)
    photo3 = models.ImageField(verbose_name="Добавить доп. фото №2", upload_to="in_stock/", blank=True)
    price = models.IntegerField(verbose_name="Цена")
    description = models.CharField(verbose_name="Описание", max_length=100)
    image_id1 = models.CharField(verbose_name="image ID 1", blank=True, null=True, editable=False)
    image_id2 = models.CharField(verbose_name="image ID 2", blank=True, null=True, editable=False)
    image_id3 = models.CharField(verbose_name="image ID 3", blank=True, null=True, editable=False)
    name_image_id1 = models.CharField(verbose_name="name_image ID 1", blank=True, null=True, editable=False)
    name_image_id2 = models.CharField(verbose_name="name_image ID 2", blank=True, null=True, editable=False)
    name_image_id3 = models.CharField(verbose_name="name_image ID 3", blank=True, null=True, editable=False)

    class Meta:
        verbose_name = 'Товар в наличии'
        verbose_name_plural = 'Товары в наличии'

