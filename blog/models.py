from django.db import models
from django.db.models.functions import Now

class Record(models.Model):
    images_dir='/static/images/'

    title = models.CharField(
        max_length=150, db_column="title", verbose_name="Заголовок"
    )
    text = models.TextField(
        max_length=5000, blank=True, db_column="description", verbose_name="Содержимое"
    )
    preview = models.ImageField(
        verbose_name="Изображение", db_column="image", blank=True, upload_to="static/blog_previews/"
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания", db_column="created_at", db_default=Now()
    )


    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["name"]
        db_table = "product"
