from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


class Traveler(models.Model):
    first_name = models.CharField('imię', max_length=100)
    last_name = models.CharField('nazwisko', max_length=100)
    email = models.EmailField('e-mail', unique=True)
    phone = models.CharField(
        'telefon',
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            r'^\+?[\d\s\-]{7,20}$',
            'Podaj poprawny numer telefonu (cyfry, spacje, myślniki, opcjonalnie +).'
        )],
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'podróżnik'
        verbose_name_plural = 'podróżnicy'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Trip(models.Model):
    destination = models.CharField('cel podróży', max_length=200)
    description = models.TextField('opis', blank=True)
    start_date = models.DateField('data rozpoczęcia')
    end_date = models.DateField('data zakończenia')
    price = models.DecimalField(
        'cena (PLN)',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    max_participants = models.PositiveIntegerField('maks. uczestników', default=10)

    class Meta:
        ordering = ['start_date']
        verbose_name = 'wycieczka'
        verbose_name_plural = 'wycieczki'

    def __str__(self):
        return f'{self.destination} ({self.start_date})'

    def spots_left(self):
        confirmed = self.reservations.filter(status='confirmed').count()
        return self.max_participants - confirmed


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Oczekująca'),
        ('confirmed', 'Potwierdzona'),
        ('cancelled', 'Anulowana'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='reservations', verbose_name='wycieczka')
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='reservations', verbose_name='podróżnik')
    created_at = models.DateTimeField('data dodania', auto_now_add=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField('uwagi', blank=True)

    class Meta:
        unique_together = ('trip', 'traveler')
        ordering = ['-created_at']
        verbose_name = 'rezerwacja'
        verbose_name_plural = 'rezerwacje'

    def __str__(self):
        return f'{self.traveler} - {self.trip}'
