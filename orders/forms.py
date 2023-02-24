from django import forms

from .models import Address, OrderDetails


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'country': forms.TextInput(attrs={'class': "form__input"}),
            'region': forms.TextInput(attrs={'class': "form__input"}),
            'city': forms.TextInput(attrs={'class': "form__input"}),
            'address': forms.TextInput(attrs={'class': "form__input"}),
            'postal_code': forms.NumberInput(attrs={'class': "form__input"}),
        }


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = '__all__'
