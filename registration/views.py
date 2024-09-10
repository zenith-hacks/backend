from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.
@login_required
def registration(request):
    return render(request, 'registration/registration.html')

@login_required
def information(request):
    if Submission.objects.filter(user=request.user).exists() and Submission.objects.get(user=request.user).submitted:
        return redirect('registration')
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            infos = form.save(commit=False)
            infos.user = request.user
            infos.address_geo = {'lat': 0, 'lng': 0} # add geolocation
            infos.distance = 0 # calculate distance
            infos.save()
            if infos.distance < 100:
                request.session['flight'] = False
            return redirect('transportation')
    if Information.objects.filter(user=request.user).exists():
        form = InformationForm(instance=Information.objects.get(user=request.user))
    else:
        form = InformationForm()
    return render(request, 'registration/information.html', {'form': form})

@login_required
def transportation(request):
    if Submission.objects.filter(user=request.user).exists() and Submission.objects.get(user=request.user).submitted:
        return redirect('registration')
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.user = request.user
            flight.flights = []
            flight.save()
            return redirect('submission')
    if Flights.objects.filter(user=request.user).exists():
        form = FlightForm(instance=Flights.objects.get(user=request.user))
    else:
        form = FlightForm()
    need_flight = request.session.get('flight', True)
    return render(request, 'registration/transportation.html', {'form': form, 'need_flight': need_flight})