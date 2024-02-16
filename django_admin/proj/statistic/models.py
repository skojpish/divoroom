from django.db import models

class User(models.Model):
    user_id = models.IntegerField(verbose_name="User Id")
    username = models.CharField(verbose_name="Username")
    enter_datetime = models.DateTimeField(verbose_name="Дата и время", null=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
