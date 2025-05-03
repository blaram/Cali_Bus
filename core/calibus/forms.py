from datetime import datetime

from django.forms import *

from core.calibus.models import Route, Travel, Client, Parcel, Bus, ParcelItem


class RouteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['origin'].widget.attrs['autofocus'] = True

    class Meta:
        model = Route
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }
        exclude = ['user_creation', 'user_updated']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TravelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['autofocus'] = True

        self.fields['departure'].widget.attrs = {
            'autocomplete': 'off',
            'class': 'form-control datetimepicker-input',
            'id': 'departure',
            'data-target': '#departure',
            'data-toggle': 'datetimepicker',
        }

    class Meta:
        model = Travel
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'departure': DateInput(format='%Y-%m-%d',
                                   attrs={
                                       'value': datetime.now().strftime('%Y-%m-%d'),
                                   }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                                       attrs={
                                           'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class TestForm(Form):
    categories = ModelChoiceField(queryset=Route.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Travel.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Travel.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class ParcelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        
        # Personalización de los campos senderID y receiverID
        self.fields['senderID'].widget.attrs['class'] = 'form-control select2'
        self.fields['senderID'].widget.attrs['style'] = 'width: 100%'
        self.fields['receiverID'].widget.attrs['class'] = 'form-control select2'
        self.fields['receiverID'].widget.attrs['style'] = 'width: 100%'

        self.fields['date_joined'].widget.attrs = {
            'autocomplete': 'off',
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'data-target': '#date_joined',
            'data-toggle': 'datetimepicker',
            'readonly': True,
        }

        # self.fields['description'].widget.attrs = {
        #    'autocomplete': 'off',
        #    'class': 'form-control',
        #    'rows': '3',
        #    'placeholder': 'Escribe aquí la descripción del paquete',
        # }

        # Personalización del campo travelID
        self.fields['travelID'].queryset = Travel.objects.filter(status=True)  # Solo viajes activos
        self.fields['travelID'].widget.attrs['class'] = 'form-control select2'
        self.fields['travelID'].widget.attrs['style'] = 'width: 100%'

    class Meta:
        model = Parcel
        fields = '__all__'
        widgets = {
            'senderID': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'receiverID': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value': datetime.now().strftime('%d-%m-%Y'),
                }
            ),
        }


class ParcelItemForm(ModelForm):
    class Meta:
        model = ParcelItem
        fields = ['description', 'quantity', 'weight', 'declared_value', 'shipping_cost']
        widgets = {
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del artículo',
            }),
            'quantity': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad',
            }),
            'weight': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso en kg',
            }),
            'declared_value': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Valor declarado',
            }),
            'shipping_cost': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Costo de envío',
            }),
        }

class BusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['license_plate'].widget.attrs['autofocus'] = True

    class Meta:
        model = Bus
        fields = '__all__'
        widgets = {
            'license_plate': TextInput(
                attrs={
                    'placeholder': 'Ingrese la placa',
                }
            ),
            'chassis_number': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de chasis',
                }
            ),
            'engine_number': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de motor',
                }
            ),
            'model': TextInput(
                attrs={
                    'placeholder': 'Ingrese el modelo',
                }
            ),
            'color': TextInput(
                attrs={
                    'placeholder': 'Ingrese el color',
                }
            ),
            'brand': TextInput(
                attrs={
                    'placeholder': 'Ingrese la marca',
                }
            ),
            'capacity': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la capacidad',
                }
            ),
            'year': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el año',
                }
            ),
            'status': CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
