from django.db import models
from django.db.models.functions import Now
from django.core.mail import send_mail
from django.conf import settings


class BlogRecord(models.Model):
    images_dir = 'static/blog_previews/'

    title = models.CharField(
        max_length=200, db_column="title", verbose_name="Заголовок"
    )
    text = models.TextField(
        max_length=5000, blank=False, verbose_name="Содержимое"
    )
    preview = models.ImageField(
        verbose_name="Изображение", blank=True, upload_to=images_dir
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    is_published = models.BooleanField(
        verbose_name="Признак публикации", db_default=False
    )

    congratulations_sent = models.BooleanField(  # чтобы не посылать поздравления более одного раза
        verbose_name="Уже поздравили", db_default=False
    )

    views_count = models.IntegerField(
        verbose_name="Количество просмотров", db_default=0
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def increment_views_count(self) -> None:
        self.views_count = self.views_count + 1
        if self.views_count > 99:
            if not self.congratulations_sent:
                text = f'Поздравляем, ваш пост от {self.created_at} с заголовком {self.title} достиг 100 просмотров!'
                send_mail('Пост достиг 100 просмотров!', text, settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL])
                # send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL])
                self.congratulations_sent = True
        self.save()

    @property
    def preview_url(self):
        if self.preview and hasattr(self.preview, 'url'):
            return self.preview.url
        else:
            return None

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"
        ordering = ["title"]
        db_table = "blog_records"
