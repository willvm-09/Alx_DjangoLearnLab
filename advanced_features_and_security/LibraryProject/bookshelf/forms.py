from django import forms
from .models import ExampleModel

class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = ['name', 'email', 'message']  # Specify the fields you want to include in the form

    # You can add custom validation, widgets, or other logic if needed
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "@example.com" in email:
            raise forms.ValidationError("Please use an @example.com email address.")
        return email
