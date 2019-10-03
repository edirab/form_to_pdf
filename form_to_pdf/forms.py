from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField
from .models import CreatePDF

'''
class PDFform(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.CharField(max_length=100)
    captcha = CaptchaField()
#    cc_myself = forms.BooleanField(required=False)
'''


class PDFform(ModelForm):
    class Meta:
        model = CreatePDF
        fields = ['sender', 'subject', 'message']

