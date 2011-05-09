from django import forms

class SMSTransferReqFormat (forms.Form):
    task = forms.CharField ()

class SMSReceivedFormat (forms.Form):
    secret  = forms.CharField ()
    message = forms.CharField ()

    def __init__ (self, *args, **kwargs):
        super (SMSReceivedFormat, self).__init__ (*args, **kwargs)
        self.fields ['from'] = forms.CharField ()
