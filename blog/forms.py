from django import forms
from .models import BlogRecord
from django.core.exceptions import ValidationError
from .mixins import FormControlMixin

FORBIDDEN_WORDS = ['казино',
                   'криптовалюта',
                   'крипта',
                   'биржа',
                   'дешево',
                   'бесплатно',
                   'обман',
                   'полиция',
                   'радар'
                   ]


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

    def clean_name(self):

        name = self.cleaned_data.get('name')

        for word in FORBIDDEN_WORDS:
            if name and (str(name).find(word) >= 0):
                raise ValidationError(f'Наименование не может содержать слово "{word}"')

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')

        for word in FORBIDDEN_WORDS:
            if description and (str(description).find(word) >= 0):
                raise ValidationError(f'Описание не может содержать слово "{word}"')

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if (price is not None) and (price <= 0.0):
            raise ValidationError(f'Цена должна быть положительным числом')

        return price