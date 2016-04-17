from django import forms


class VisitorMessageForm(forms.Form):
    message = forms.CharField(label='Your message', max_length=100)




