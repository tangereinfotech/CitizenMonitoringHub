from django.http import HttpResponse
from django.shortcuts import render_to_response

def index (request):
    request.session.set_expiry (0) # FIXME: Change this to a reasonable timeout
    return render_to_response ('index.html')

