from django import forms
from .models import BlogRecord
from django.core.exceptions import ValidationError
from django.conf import settings
from .mixins import FormControlMixin


class BlogRecordCreateForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = BlogRecord
        fields = ['title', 'text', 'preview', 'is_published', 'views_count']

    def __init__(self, *args, **kwargs):
        super(BlogRecordCreateForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'placeholder': 'Введите заголовок'  # Текст подсказки внутри поля
        })

        self.fields['text'].widget.attrs.update({
            'placeholder': 'Введите текст записи'  # Текст подсказки внутри поля
        })

        self.fields['is_published'].widget.attrs.update({
            'class': 'custom-checkbox-class'
        })

        # self.fields['price'].widget.attrs.update({
        #     'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        # })
        #
        #
        # self.fields['category'].widget.attrs.update({
        #     'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        # })
        #
        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        # })

        # # Настройка атрибутов виджета для поля 'enrollment_date'
        # self.fields['enrollment_date'].widget.attrs.update({
        #     'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        #     'type': 'date'  # Указание типа поля как даты
        # })

    def clean_name(self):

        name = self.cleaned_data.get('name')

        for word in settings.FORBIDDEN_WORDS:
            if name and (str(name).find(word) >= 0):
                raise ValidationError(f'Наименование не может содержать слово "{word}"')

        return name


    def clean_description(self):
        description = self.cleaned_data.get('description')

        for word in settings.FORBIDDEN_WORDS:
            if description and (str(description).find(word) >= 0):
                raise ValidationError(f'Описание не может содержать слово "{word}"')

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if (price is not None) and (price <= 0.0):
            raise ValidationError(f'Цена должна быть положительным числом')

        return price

    # def clean(self):

    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     description = cleaned_data.get('description')
    #
    #     for word in forbidden_words:
    #         if name and (str(name).find(word) >= 0):
    #             self.add_error('name', f'Наименование не может содержать слово "{word}"')
    #         if description and (str(description).find(word) >= 0):
    #             self.add_error('description', f'Описание не может содержать слово "{word}"')



"""
class BlogRecordCreateForm(forms.Form):
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
        related_name="BlogRecords",
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
