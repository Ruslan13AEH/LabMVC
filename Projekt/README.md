# Organizacja podróży

Prosta aplikacja webowa w Django do zarządzania wycieczkami i rezerwacjami. Można dodawać wycieczki, podróżników i przypisywać ich do wyjazdów.

## Co robi aplikacja

- dodawanie, edytowanie i usuwanie wycieczek
- dodawanie, edytowanie i usuwanie podróżników
- rezerwacje – można przypisać podróżnika do wycieczki, ustawić status (oczekująca / potwierdzona / anulowana)
- automatyczne liczenie wolnych miejsc
- filtrowanie wycieczek po dacie i miejscu docelowym
- walidacja formularzy (daty, e-mail, telefon itp.)
- panel admina Django

## MVC

- modele są w `travels/models.py` (Trip, Traveler, Reservation)
- widoki (logika) są w `travels/views.py`
- szablony HTML są w `travels/templates/travels/`
- formularze w `travels/forms.py`
- routing w `travels/urls.py`

## Jak uruchomić

```bash
cd Projekt
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Opcjonalnie można wczytać przykładowe dane:

```bash
python manage.py loaddata travels/fixtures/sample_data.json
```

Aplikacja działa pod adresem http://127.0.0.1:8000/

## Testy

```bash
python manage.py test travels
```

## Przykładowe dane

W pliku `travels/fixtures/sample_data.json` są 4 wycieczki (Rzym, Paryż, Barcelona, Wiedeń), 4 podróżników i 4 rezerwacje.

Wczytaj je poleceniem:

```bash
python manage.py loaddata travels/fixtures/sample_data.json
```