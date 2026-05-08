import datetime
from django import forms
from .models import Trip, Traveler, Reservation


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'description', 'start_date', 'end_date', 'price', 'max_participants']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make Bootstrap-friendly
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        # Set HTML5 min for date fields
        today = datetime.date.today().isoformat()
        self.fields['start_date'].widget.attrs['min'] = today
        self.fields['end_date'].widget.attrs['min'] = today

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError('Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.')
        return cleaned_data


class TravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ['first_name', 'last_name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['traveler', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        if trip:
            # Exclude travelers who already have a reservation for this trip
            existing_ids = trip.reservations.values_list('traveler_id', flat=True)
            self.fields['traveler'].queryset = Traveler.objects.exclude(id__in=existing_ids)
