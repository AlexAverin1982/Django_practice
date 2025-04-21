from django.db import models
from django.db.models.functions import Now


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование', db_column='name')
    description = models.TextField(max_length=500, verbose_name='Описание', blank=True, db_column='description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
        db_table = 'category'


class Product(models.Model):
    name = models.CharField(max_length=150, db_column='name', verbose_name='Наименование')
    description = models.TextField(max_length=500, blank=True, db_column='description', verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', db_column='image', blank=True, upload_to='photos/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category', related_name='products')
    price = models.FloatField(verbose_name='Цена за покупку', db_column='price', default=0.0)
    created_at = models.DateTimeField(verbose_name='Дата создания', db_column='created_at', db_default=Now())
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', db_column='updated_at',
                                      db_default=Now())

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
        db_table = 'product'

class ContactsInfo(models.Model):
    email = models.EmailField(db_column='email', verbose_name='Электронная почта')
    telegram = models.CharField(max_length=150, db_column='telegram', verbose_name='Телеграм')
    vk_group = models.URLField(max_length=150, db_column='vkgroup', verbose_name='Группа ВКонтакте')
    # description = models.TextField(max_length=500, blank=True, db_column='description', verbose_name='Описание')
    # image = models.ImageField(verbose_name='Изображение', db_column='image', blank=True, upload_to='photos/')
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category', related_name='products')
    # price = models.FloatField(verbose_name='Цена за покупку', db_column='price', default=0.0)
    # created_at = models.DateTimeField(verbose_name='Дата создания', db_column='created_at', db_default=Now())
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', db_column='updated_at',
                                      db_default=Now())

    def __str__(self):
        return f'Электронная почта: {self.email}\nТелеграм: {self.telegram}\nГруппа ВКонтакте: {self.vk_group}'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
        ordering = ['updated_at', 'email', 'telegram']
        db_table = 'contacts'