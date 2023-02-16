from django import forms

from carts.models import Cart


class CartForm(forms.ModelForm):
    quantity = forms.IntegerField(label='',
                                  # disabled=True,
                                  widget=forms.NumberInput(attrs={
                                      'class': 'quantity-input',
                                  }))
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Cart
        # fields = '__all__'
        fields = ('quantity', 'DELETE',)


SetCartForms = forms.modelformset_factory(Cart, CartForm, extra=0)

# class SetCartForms(forms.BaseModelFormSet):
#     model = Cart
