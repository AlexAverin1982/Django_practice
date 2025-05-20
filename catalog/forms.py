from django import forms
from .models import Product
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

class ProductCreateForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите краткое наименование'  # Текст подсказки внутри поля
        })

        self.fields['description'].widget.attrs.update({
            'placeholder': 'Введите описание'  # Текст подсказки внутри поля
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
