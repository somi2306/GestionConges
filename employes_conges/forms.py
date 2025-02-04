from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Employee, LeaveRequest

class EmployeeRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Nom d\'utilisateur',
        max_length=150,
        help_text='',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$', 
                message='Saisissez un nom d\'utilisateur valide.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Adresse email'
        })
    )
    
    first_name = forms.CharField(
        label='Prénom',
        
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Prénom '
        })
    )
    
    last_name = forms.CharField(
        label='Nom',
        
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nom de famille '
        })
    )
    
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Mot de passe'
        }),
        help_text=''
    )
    
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirmer le mot de passe'
        }),
        help_text=''
    )

    class Meta:
        model = Employee
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Vérifications personnalisées du mot de passe
        if len(password) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        
        # Vérification qu'il n'est pas entièrement numérique
        if password.isdigit():
            raise ValidationError('Le mot de passe ne peut pas être entièrement numérique.')
        
        # Vérification que le mot de passe n'est pas trop similaire aux informations personnelles
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        
        if (username and username.lower() in password.lower()) or \
           (first_name and first_name.lower() in password.lower()) or \
           (last_name and last_name.lower() in password.lower()):
            raise ValidationError('Le mot de passe ne doit pas être trop similaire à vos informations personnelles.')
        
        return password

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError('La date de début doit être antérieure ou égale à la date de fin.')
        
        return cleaned_data