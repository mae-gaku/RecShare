from django import forms
from .models import Store, Review, StoreGroup
from django.forms import inlineformset_factory

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'website', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'hours', 'website', 'image', 'latitude', 'longitude', 'genre']



class StoreGroupForm(forms.ModelForm):
    class Meta:
        model = StoreGroup
        fields = ['name', 'stores']
        widgets = {
            'stores': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'グループ名',
            'stores': '含めるお店',
        }