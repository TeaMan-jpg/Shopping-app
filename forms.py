from django import forms
from .models import Product,Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','price','desc','quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product quantity'
            })
        }

    
 
class ReviewForm(forms.ModelForm):

    
    

    class Meta:
        model = Review
        fields = ['title','rating','desc']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_class = 'form-horizontal'

