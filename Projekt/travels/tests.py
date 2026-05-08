import datetime
from django.test import TestCase
from django.urls import reverse

from .models import Trip, Traveler, Reservation
from .forms import TripForm, TravelerForm


class TravelerModelTest(TestCase):
    def setUp(self):
        self.traveler = Traveler.objects.create(
            first_name='Anna', last_name='Kowalska', email='anna@example.com'
        )

    def test_str(self):
        self.assertEqual(str(self.traveler), 'Anna Kowalska')

    def test_email_stored(self):
        self.assertEqual(self.traveler.email, 'anna@example.com')


class TripModelTest(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            destination='Rzym',
            start_date=datetime.date(2026, 6, 1),
            end_date=datetime.date(2026, 6, 10),
            price='1500.00',
            max_participants=5,
        )

    def test_str(self):
        self.assertIn('Rzym', str(self.trip))

    def test_spots_left_no_reservations(self):
        self.assertEqual(self.trip.spots_left(), 5)

    def test_spots_left_with_confirmed_reservation(self):
        traveler = Traveler.objects.create(
            first_name='Jan', last_name='Nowak', email='jan@example.com'
        )
        Reservation.objects.create(trip=self.trip, traveler=traveler, status='confirmed')
        self.assertEqual(self.trip.spots_left(), 4)

    def test_spots_left_ignores_pending(self):
        traveler = Traveler.objects.create(
            first_name='Jan', last_name='Nowak', email='jan@example.com'
        )
        Reservation.objects.create(trip=self.trip, traveler=traveler, status='pending')
        self.assertEqual(self.trip.spots_left(), 5)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            destination='Paryż',
            start_date=datetime.date(2026, 7, 1),
            end_date=datetime.date(2026, 7, 7),
            price='2000.00',
        )
        self.traveler = Traveler.objects.create(
            first_name='Ewa', last_name='Wiśniewska', email='ewa@example.com'
        )
        self.reservation = Reservation.objects.create(
            trip=self.trip, traveler=self.traveler
        )

    def test_str(self):
        self.assertIn('Paryż', str(self.reservation))
        self.assertIn('Ewa', str(self.reservation))

    def test_default_status_is_pending(self):
        self.assertEqual(self.reservation.status, 'pending')


class TripFormValidationTest(TestCase):
    def _base_data(self, **kwargs):
        data = {
            'destination': 'Londyn',
            'start_date': '2026-08-01',
            'end_date': '2026-08-10',
            'price': '1200.00',
            'max_participants': 8,
        }
        data.update(kwargs)
        return data

    def test_valid_form(self):
        form = TripForm(data=self._base_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_end_before_start_invalid(self):
        form = TripForm(data=self._base_data(start_date='2026-08-10', end_date='2026-08-01'))
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_missing_destination_invalid(self):
        form = TripForm(data=self._base_data(destination=''))
        self.assertFalse(form.is_valid())
        self.assertIn('destination', form.errors)

    def test_negative_price_invalid(self):
        form = TripForm(data=self._base_data(price='-100'))
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)


class TravelerFormValidationTest(TestCase):
    def test_invalid_email(self):
        form = TravelerForm(data={
            'first_name': 'Jan', 'last_name': 'Nowak',
            'email': 'not-an-email', 'phone': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_form(self):
        form = TravelerForm(data={
            'first_name': 'Jan', 'last_name': 'Nowak',
            'email': 'jan@example.com', 'phone': '+48 600 100 200',
        })
        self.assertTrue(form.is_valid(), form.errors)


class TripListViewTest(TestCase):
    def setUp(self):
        Trip.objects.create(
            destination='Barcelona',
            start_date=datetime.date(2026, 9, 1),
            end_date=datetime.date(2026, 9, 8),
            price='1800.00',
        )
        Trip.objects.create(
            destination='Wiedeń',
            start_date=datetime.date(2026, 10, 1),
            end_date=datetime.date(2026, 10, 5),
            price='900.00',
        )

    def test_list_returns_200(self):
        response = self.client.get(reverse('trip_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_all_trips(self):
        response = self.client.get(reverse('trip_list'))
        self.assertContains(response, 'Barcelona')
        self.assertContains(response, 'Wiedeń')

    def test_search_filters_results(self):
        response = self.client.get(reverse('trip_list'), {'q': 'barcelona'})
        self.assertContains(response, 'Barcelona')
        self.assertNotContains(response, 'Wiedeń')


class TripDetailViewTest(TestCase):
    def setUp(self):
        self.trip = Trip.objects.create(
            destination='Madryt',
            start_date=datetime.date(2026, 11, 1),
            end_date=datetime.date(2026, 11, 7),
            price='1600.00',
        )

    def test_detail_returns_200(self):
        response = self.client.get(reverse('trip_detail', args=[self.trip.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_shows_destination(self):
        response = self.client.get(reverse('trip_detail', args=[self.trip.pk]))
        self.assertContains(response, 'Madryt')


class TripCreateViewTest(TestCase):
    def test_get_returns_200(self):
        response = self.client.get(reverse('trip_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_trip_and_redirects(self):
        response = self.client.post(reverse('trip_create'), {
            'destination': 'Lizbona',
            'start_date': '2026-12-01',
            'end_date': '2026-12-08',
            'price': '1400.00',
            'max_participants': 10,
        })
        self.assertEqual(Trip.objects.filter(destination='Lizbona').count(), 1)
        self.assertEqual(response.status_code, 302)
