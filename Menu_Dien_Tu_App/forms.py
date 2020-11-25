from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class ContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True, max_length=100, widget=forms.TextInput(attrs={'type': 'text', 'id': 'form-contact-name', 'class': "form-control"}))
    contact_email = forms.EmailField(
        required=True, max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'type': 'textarea', 'id': "form-contact-message", 'class': "form-control md-textarea", 'rows': "4"}))

    def __str__(seft):
        return str(self.contact_name) + "-" + str(self.contact_name) + " : " + str(self.content)
