
from django.http import HttpResponse
from django.shortcuts import redirect

def hola_mundo(request):
    return HttpResponse("HOLA MUNDO")

def root_redirect(request):
    return redirect('/graphql/')