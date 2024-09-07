from django import forms
from .models import Store, Dish
from django.forms import inlineformset_factory

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'website', 'image']

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['store', 'name', 'description', 'image', 'price']

# Storeに関連するDishを一度に入力できるようにするフォームセット
DishFormSet = inlineformset_factory(Store, Dish, form=DishForm, extra=1, can_delete=True)



