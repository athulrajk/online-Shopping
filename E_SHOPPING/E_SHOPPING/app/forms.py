from django.forms import ModelForm 
from django.core.exceptions import ValidationError
from.models import Product,User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import validate_email


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'address', 'city', 'pincode', 'password1', 'password2']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean_name(self):
            name = self.cleaned_data.get('name')
            if any(char.isdigit() for char in name):
                raise ValidationError("Name cannot contain numbers.")
            return name
    
    def clean_email(self):
        email =self.cleaned_data.get('email')
        try:
             validate_email(email)
        except ValidationError:
             raise ValidationError("Invalid Email id")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use")
        return email
    
    def clean_phone(self):
        phone_number = self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone number is already in use")
        if not phone_number.isdigit():
            raise ValidationError("Phone number should contain only digits")
        if len(phone_number) != 10:
            raise ValidationError("Phone number should be 10 digits long")
        return phone_number


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProductRegistration(ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if any(char.isdigit() for char in name):
                raise ValidationError("Name cannot contain numbers.")
            return name
        
        def clean_price(self):
                price = self.cleaned_data.get('price')
                if price is not None and price < 0:
                    raise ValidationError("Price cannot be negative.")
                return price
        
        def clean_files(self):
            files = self.cleaned_data.get('files')
            if files:
                if not files.name.endswith(('.jpg', '.png')):
                    raise ValidationError("Only .jpg and .png files are allowed.")
            return files
        
        class Meta: 
            model = Product
            exclude = ('status','updation',)
