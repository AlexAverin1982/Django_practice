from django import forms
from .models import Category, Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image', 'description']

"""
class ProductCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label="Наименование")
    description = forms.CharField(widget=forms.Textarea, initial="Описание товара", required=False)
    
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    description = models.TextField(
        max_length=500, blank=True, db_column="description", verbose_name="Описание"
    )
    image = models.ImageField(
        verbose_name="Изображение", db_column="image", blank=True, upload_to="static/images/"
    )
    # image = models.CharField(
    #     verbose_name="Изображение", db_column="image", blank=True
    # )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column="category",
        related_name="products",
    )
    price = models.FloatField(
        verbose_name="Цена за покупку", db_column="price", default=0.0
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", db_column="created_at", db_default=Now()
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата последнего изменения",
        db_column="updated_at",
        db_default=Now(),
    )
    
    """