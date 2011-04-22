from django import forms

class SMSTransferReqFormat (forms.Form):
    task = forms.CharField ()

class SMSReceivedFormat (forms.Form):
    secret  = forms.CharField ()
    fromu   = forms.CharField ()
    message = forms.CharField ()
