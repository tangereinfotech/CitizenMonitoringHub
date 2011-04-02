from django import forms
from django.contrib.auth.models import User
from cmh.captcha.fields import CaptchaField
import re

class UserLoginForm (forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #captcha  = CaptchaField()

class UserRegisterForm(forms.Form):
    username        = forms.CharField(label="username", max_length=30)
    password        = forms.CharField(label="password", widget=forms.PasswordInput)
    repassword      = forms.CharField(label="repassword", widget=forms.PasswordInput)
    fname           = forms.CharField(label="fname", max_length=30)
    lname           = forms.CharField(label="lname", max_length=30)
    streetaddress   = forms.CharField(label="streetaddress", max_length=100)
    town            = forms.CharField(label="town", max_length=50)
    district        = forms.CharField(label="district", max_length=50)
    state           = forms.CharField(label="state", max_length=50)
    pincode         = forms.IntegerField(label="pincode")
    phone           = forms.CharField(label="phone"  ,max_length=15)
    mobile          = forms.CharField(label="mobile" ,max_length=15)
    email           = forms.EmailField(label="email")
    captcha  = CaptchaField()
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if (re.match('^([a-zA-Z_0-9]|[_.])+$',username) !=None):
            try:
                user = User.objects.get(username=username)
                raise forms.ValidationError("Username already Exist")
            except User.DoesNotExist:
                return username            
        else:
            raise forms.ValidationError("Username format is invalid")
        
    
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if (re.match('^\+?\d{4,15}$',mobile) !=None):
            return mobile
        else:
            raise forms.ValidationError("Mobile number format is invalid")
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if (re.match('^\+?\d{4,15}$',phone) !=None):
            return phone
        else:
            raise forms.ValidationError("Phone number format is invalid")
    
