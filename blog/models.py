from django.db import models
from django.db.models.functions import Now

class BlogRecord(models.Model):
    images_dir='static/blog_previews/'

    title = models.CharField(
        max_length=200, db_column="title", verbose_name="Заголовок"
    )
    text = models.TextField(
        max_length=5000, blank=False, verbose_name="Содержимое"
    )
    preview = models.ImageField(
        verbose_name="Изображение", blank=True, upload_to=images_dir
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания", db_default=Now(),
    )

    is_published = models.BooleanField(
        verbose_name="Признак публикации", db_default=False
    )

    views_count = models.IntegerField(
        verbose_name="Количество просмотров", db_default=0
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def increment_views_count(self) -> None:
        self.views_count = self.views_count + 1
        self.save()

    @property
    def preview_url(self):
        if self.preview and hasattr(self.preview, 'url'):
            return self.preview.url

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"
        ordering = ["title"]
        db_table = "blog_records"
