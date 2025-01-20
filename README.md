# Projekt Analizy Opon letnich na podstawie danych z dwóch sklepów internetowych - Sklep Opon i Oponeo

## Opis projektu

Projekt realizuje przetwarzanie danych o cenach opon, począwszy od scrapowania danych z dwóch sklepów internetowych, poprzez ich czyszczenie, analizę i modelowanie, aż po budowę aplikacji w Streamlit umożliwiającej interakcję z wynikami.

Główne funkcjonalności:
- Scrapowanie danych ze sklepów internetowych.
- Eksploracyjna analiza danych i wizualizacje.
- Modele przewidywania cen i rekomendacji produktów.
- Aplikacja Streamlit z trzema zakładkami: przewidywanie cen, rekomendacje, wyszukiwarka opon.

---

## Struktura projektu

### Pliki i foldery
- **`main.ipynb`**: Notebook z całym pipeline'em projektu:
  - **0. Importy**: Importowanie wymaganych bibliotek.
  - **1. Scrapowanie danych**: Pobieranie danych z dwóch sklepów.
  - **2. Czyszczenie i przygotowanie danych**: Przygotowanie danych do analizy.
  - **3. Eksploracyjna analiza danych**: Analiza korelacji, trendów i rozkładów.
  - **4. Wizualizacja danych**: Tworzenie wykresów.
  - **5. Porównanie sklepów i wnioski**: Analiza cen i dostępności.
  - **6. Uczenie modeli**: Trening modelu Random Forest Regressor.

- **`gui/app.py`**: Aplikacja Streamlit z trzema zakładkami:
  - **Przewidywanie ceny**: Model przewidujący ceny na podstawie parametrów.
  - **Rekomendacje opon**: Model rekomendacji opon na podstawie danych.
  - **Wyszukiwarka opon**: Dynamiczne przeglądanie i filtrowanie danych.

- **`scrappers/`**: Moduły scrapujące dane:
  - `sklep_opon.py`
  - `oponeo.py`

- **`common/`**: Moduły pomocnicze:
  - `file_utils.py`: Funkcje do ładowania i obsługi danych.

### Struktura aplikacji Streamlit
- **Zakładka 1: Przewidywanie ceny**: Pozwala przewidywać cenę na podstawie wybranych parametrów.
- **Zakładka 2: Rekomendacje opon**: Generuje rekomendacje na podstawie analizy.
- **Zakładka 3: Wyszukiwarka opon**: Pozwala dynamicznie wyszukiwać i filtrować dane o oponach.

---

## Instrukcja uruchomienia

### Uruchomienie notebooka:
1. **Jeśli nie masz danych**:
   - Uruchom wszystkie komórki w pliku `main.ipynb` po kolei.
   - **Uwaga**: Proces scrapowania danych jest czasochłonny.
2. **Jeśli masz dane i chcesz pominąć scrapowanie**:
   - Otwórz `main.ipynb` i uruchom sekcje w następującej kolejności:
     - **0. Importy**
     - **2.1 Tworzenie metod pomocniczych**
     - **3. Ładowanie danych**
   - Następnie przejdź do dalszych sekcji zgodnie z potrzebami.

### Uruchomienie aplikacji Streamlit:
1. W terminalu przejdź do głównego folderu projektu.
2. Uruchom aplikację komendą:
   ```bash
   streamlit run ./gui/app.py


### Wymagania
- Python 3.12
- streamlit - 1.41.1
- pandas - 2.2.3
- selenium - 4.27.1
- matplotlib - 3.10.0
- scikit-learn - 1.6.0
- seaborn - 0.13.2
- ipython - 8.30.0
