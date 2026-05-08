from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Trip, Traveler, Reservation
from .forms import TripForm, TravelerForm, ReservationForm


def trip_list(request):
    trips = Trip.objects.all()
    query = request.GET.get('q', '').strip()
    start_from = request.GET.get('start_from', '')
    start_to = request.GET.get('start_to', '')

    if query:
        trips = trips.filter(destination__icontains=query)
    if start_from:
        trips = trips.filter(start_date__gte=start_from)
    if start_to:
        trips = trips.filter(start_date__lte=start_to)

    return render(request, 'travels/trip_list.html', {
        'trips': trips,
        'query': query,
        'start_from': start_from,
        'start_to': start_to,
    })


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    reservations = trip.reservations.select_related('traveler')
    return render(request, 'travels/trip_detail.html', {
        'trip': trip,
        'reservations': reservations,
    })


def trip_create(request):
    form = TripForm(request.POST or None)
    if form.is_valid():
        trip = form.save()
        messages.success(request, 'Wycieczka została dodana.')
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'travels/trip_form.html', {
        'form': form,
        'title': 'Dodaj wycieczkę',
    })


def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    form = TripForm(request.POST or None, instance=trip)
    if form.is_valid():
        form.save()
        messages.success(request, 'Wycieczka została zaktualizowana.')
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'travels/trip_form.html', {
        'form': form,
        'title': 'Edytuj wycieczkę',
        'trip': trip,
    })


def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Wycieczka została usunięta.')
        return redirect('trip_list')
    return render(request, 'travels/trip_confirm_delete.html', {'trip': trip})


def traveler_list(request):
    travelers = Traveler.objects.all()
    query = request.GET.get('q', '').strip()
    if query:
        travelers = travelers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'travels/traveler_list.html', {
        'travelers': travelers,
        'query': query,
    })


def traveler_create(request):
    form = TravelerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Podróżnik został dodany.')
        return redirect('traveler_list')
    return render(request, 'travels/traveler_form.html', {
        'form': form,
        'title': 'Dodaj podróżnika',
    })


def traveler_edit(request, pk):
    traveler = get_object_or_404(Traveler, pk=pk)
    form = TravelerForm(request.POST or None, instance=traveler)
    if form.is_valid():
        form.save()
        messages.success(request, 'Dane podróżnika zostały zaktualizowane.')
        return redirect('traveler_list')
    return render(request, 'travels/traveler_form.html', {
        'form': form,
        'title': 'Edytuj podróżnika',
        'traveler': traveler,
    })


def traveler_delete(request, pk):
    traveler = get_object_or_404(Traveler, pk=pk)
    if request.method == 'POST':
        traveler.delete()
        messages.success(request, 'Podróżnik został usunięty.')
        return redirect('traveler_list')
    return render(request, 'travels/traveler_confirm_delete.html', {'traveler': traveler})


def reservation_create(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    form = ReservationForm(request.POST or None, trip=trip)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.trip = trip
        reservation.save()
        messages.success(request, 'Rezerwacja została dodana.')
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'travels/reservation_form.html', {
        'form': form,
        'trip': trip,
    })


def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    trip_pk = reservation.trip.pk
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Rezerwacja została usunięta.')
        return redirect('trip_detail', pk=trip_pk)
    return render(request, 'travels/reservation_confirm_delete.html', {'reservation': reservation})
