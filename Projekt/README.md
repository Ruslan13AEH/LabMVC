# Organizacja podróży – Platforma do organizacji podróży i wyjazdów

## Spis treści

1. [Opis projektu](#opis-projektu)
2. [Funkcjonalności](#funkcjonalności)
3. [Wzorzec MVC](#wzorzec-mvc)
4. [Uruchomienie aplikacji](#uruchomienie-aplikacji)
5. [Przykładowe dane](#przykładowe-dane)

---

## Opis projektu

Organizacja podróży to aplikacja webowa zbudowana w Django (Python) umożliwiająca zarządzanie wycieczkami i wyjazdami grupowymi. Użytkownik może tworzyć wycieczki, dodawać podróżników oraz przypisywać ich do wycieczek przez system rezerwacji.

---

## Funkcjonalności

| Funkcja | Opis |
|---|---|
| **CRUD wycieczek** | Tworzenie, przeglądanie, edycja i usuwanie wycieczek (cel podróży, daty, cena, maks. uczestników) |
| **CRUD podróżników** | Zarządzanie uczestnikami wyjazdów (imię, nazwisko, e-mail, telefon) |
| **Rezerwacje** | Dodawanie i usuwanie rezerwacji łączących podróżnika z wycieczką; statusy: oczekująca / potwierdzona / anulowana |
| **Wolne miejsca** | Automatyczne obliczanie wolnych miejsc na podstawie potwierdzonych rezerwacji |
| **Wyszukiwanie i filtrowanie** | Filtrowanie wycieczek po celu podróży i zakresie dat; wyszukiwanie podróżników po imieniu, nazwisku lub e-mailu |
| **Walidacja po stronie serwera** | Formularze Django sprawdzają wymagane pola, format e-mail, numer telefonu, ujemną cenę oraz poprawność dat (koniec ≥ start) |
| **Walidacja po stronie klienta** | HTML5 (`type="date"`, `type="email"`, `min`, `required`) oraz Bootstrap 5 Validation API |
| **Ostylowane widoki** | Bootstrap 5 – responsywna tabela z kolorowymi badge'ami, ikony Bootstrap Icons, karty szczegółów |
| **Testy jednostkowe** | Testy modeli, formularzy i widoków (`python manage.py test`) |
| **Panel administratora** | Django Admin z zarejestrowanymi modelami Trip, Traveler, Reservation |

---

## Wzorzec MVC

| Warstwa | Pliki |
|---|---|
| **Model** | `travels/models.py` – klasy `Trip`, `Traveler`, `Reservation` z walidatorami i relacjami ForeignKey |
| **Widok (View/Template)** | `travels/templates/travels/*.html` – szablony Django dziedziczące z `base.html` |
| **Kontroler (View)** | `travels/views.py` – funkcje obsługujące żądania HTTP, komunikujące się z modelami i przekazujące dane do szablonów |
| **Formularze** | `travels/forms.py` – `TripForm`, `TravelerForm`, `ReservationForm` z logiką walidacji |
| **URL routing** | `travels/urls.py`, `travel_project/urls.py` |

---

## Uruchomienie aplikacji

### Wymagania

- Python 3.10+
- pip

### Kroki

```bash
# 1. Przejdź do katalogu projektu
cd Projekt

# 2. (Opcjonalnie) Utwórz środowisko wirtualne
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Utwórz i zastosuj migracje bazy danych
python manage.py makemigrations
python manage.py migrate

# 5. (Opcjonalnie) Wczytaj przykładowe dane
python manage.py loaddata travels/fixtures/sample_data.json

# 6. (Opcjonalnie) Utwórz konto administratora
python manage.py createsuperuser

# 7. Uruchom serwer deweloperski
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:8000/**  
Panel administratora: **http://127.0.0.1:8000/admin/**

### Uruchamianie testów

```bash
python manage.py test travels
```

---

## Przykładowe dane

Plik `travels/fixtures/sample_data.json` zawiera:
- 4 podróżników
- 4 wycieczki (Rzym, Paryż, Barcelona, Wiedeń)
- 4 rezerwacje

Wczytaj je poleceniem:

```bash
python manage.py loaddata travels/fixtures/sample_data.json
```