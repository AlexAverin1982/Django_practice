
class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super(FormControlMixin, self).__init__(*args, **kwargs)

        for field_name in self.fields.keys():  # получаем название полей

            self.fields[field_name].widget.attrs.update({  # присваеваем значения полям на основании перебора
                'class': 'form-control',
            })

