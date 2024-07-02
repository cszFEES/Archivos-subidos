from django.shortcuts import render, redirect
from .models import Perfiles

def home(request):
    return render(request, 'home.html')

def mecenas(request):
    return render(request, 'mecenas.html', {'Perfiles':Perfiles.objects.all()})

def mecenazgo(request):
    #Perfiles.objects.all().delete()
    if request.method == 'POST':
        mote1 = request.POST['mote']
        desc1 = request.POST['desc']
        mayorDeEdad1 = request.POST.get('mayorDeEdad', False)
        Perfiles.objects.create(mote=mote1, desc=desc1, mayorDeEdad=mayorDeEdad1)
        print(Perfiles.objects.all())
        return redirect('mecenas')

    return render(request, 'mecenazgo.html', {'Perfiles':Perfiles})