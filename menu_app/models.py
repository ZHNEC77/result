from django.db import models

# Create your models here.


class Menu(models.Model):
    title = models.CharField(
        max_length=77,
        unique=True,
        verbose_name='Заголовок'
    )
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Название меню'
        verbose_name_plural = 'Названия меню'


class MenuItem(models.Model):
    name = models.CharField(
        max_length=77,
        unique=True,
        null=False,
        blank=False,
    )
    url = models.CharField(max_length=255)
    menu = models.ForeignKey(
        to=Menu,
        on_delete=models.CASCADE,
        blank=True,
        related_name='items',
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
