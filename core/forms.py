from django import forms
from core.models import Product
from core.models import Brand
from core.models import Supplier
from core.models import Category
from django import forms

class ProductForm(forms.ModelForm):
    price = forms.IntegerField(min_value=1, max_value=250)
    stock = forms.IntegerField(min_value=1, max_value=250)

    class Meta:
        model = Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["description", "image"]
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name','ruc','address','phone']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description']
        

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
