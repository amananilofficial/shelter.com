from django import forms

class QuickContactForm(forms.Form):
    name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your name'}))
    email = forms.CharField(label='', required=True, widget=forms.EmailInput(attrs={'placeholder':'Enter your E-mail address'}))
    phone = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your phone number'}))