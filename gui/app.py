import streamlit as st
import pandas as pd
import joblib
import sys
import os

# Dodanie katalogu głównego projektu do ścieżki, żeby ładowało modele
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.TyreModels import TyreSizeData


def load_pipeline_data():
    pipeline = joblib.load('data/models/tyres_pipeline.pkl')
    df = pd.read_csv('data/models/tyres_data.csv')
    return pipeline, df

def get_profiles(diameter):
    return sorted(set([t.profile for t in TyreSizeData.TYRE_DATA if t.diameter == diameter]))

def get_widths(diameter, profile):
    return sorted(set([t.width for t in TyreSizeData.TYRE_DATA if t.diameter == diameter and t.profile == profile]))

# Wczytaj model, scaler i dane
pipeline, df = load_pipeline_data()
df = df.dropna()

# Interfejs Streamlit
st.title("Rekomendacje Opon")

# Wprowadzenie parametrów użytkownika
max_price = st.number_input("Maksymalna cena (PLN):", min_value=0.0, value=500.0, step=1.0)
max_user_rating = df['user_rating'].max()
min_rating = st.slider("Minimalna ocena użytkownika:", min_value=1.0, max_value=max_user_rating, step=0.1, value=4.0)

# Rozmiar opony
selected_diameter = st.selectbox("Średnica opony (R):", sorted(set([t.diameter for t in TyreSizeData.TYRE_DATA])))
available_profiles = get_profiles(selected_diameter)
selected_profile = st.selectbox("Profil opony:", available_profiles)
available_widths = get_widths(selected_diameter, selected_profile)
selected_width = st.selectbox("Szerokość opony:", available_widths)

size_filter = f"{selected_width}/{selected_profile} R{selected_diameter}"

# Marka (opcjonalnie)
brand = st.text_input("Preferowana marka (opcjonalnie):")

# Klasa opony (opcjonalnie)
available_classes = df['class'].unique() if 'class' in df.columns else []
selected_class = st.selectbox("Klasa opony (opcjonalnie):", options=[""] + list(available_classes))

# Kliknięcie przycisku rekomendacji
if st.button("Rekomenduj"):
    # Filtrowanie danych na podstawie preferencji użytkownika
    filtered_df = df[
        (df['price'] <= max_price) &
        (df['user_rating'] >= min_rating) &
        (df['size'] == size_filter)
    ]

    if brand:
        filtered_df = filtered_df[filtered_df['brand'] == brand]

    if selected_class:
        filtered_df = filtered_df[filtered_df['class'] == selected_class]

    # Jeśli brak wyników, wyświetl najlepsze ogólne wyniki
    if filtered_df.empty:
        st.warning("Brak wyników spełniających kryteria. Wyświetlam najlepsze ogólne wyniki.")
        filtered_df = df.copy()

    # Przygotowanie danych wejściowych dla modelu
    columns_to_drop = ['name', 'brand', 'model']
    columns_to_drop = [col for col in columns_to_drop if col in filtered_df.columns]
    X_filtered = filtered_df.drop(columns=columns_to_drop, errors='ignore')

    # Użycie pipeline do przetworzenia danych i predykcji
    try:
        predicted_target = pipeline.predict(X_filtered)
    except Exception as e:
        st.error(f"Błąd podczas predykcji: {e}")
        st.stop()

    # Dodanie predykcji do DataFrame
    filtered_df = filtered_df.copy()  # Uniknięcie SettingWithCopyWarning
    filtered_df['predicted_target'] = predicted_target

    # Sortowanie i wybór top_n
    top_n = 3
    filtered_df_sorted = filtered_df.sort_values(by='predicted_target', ascending=False)
    recommendations = filtered_df_sorted.head(top_n)

    selected_columns = {
        "name": "Nazwa",
        "brand": "Marka",
        "model": "Model",
        "size": "Rozmiar",
        "load_index": "Indeks nośności",
        "speed_index": "Indeks prędkości",
        "wet_grip_index": "Przyczepność na mokrej nawierzchni",
        "noise_index": "Indeks hałasu",
        "noise_level": "Poziom hałasu",
        "class": "Klasa",
        "user_rating": "Ocena użytkownika",
        "price": "Cena",
        "availability": "Dostępność",
        "retailer": "Sprzedawca"
    }

    # Wyświetlenie wyników
    if recommendations.empty:
        st.warning("Brak wyników spełniających kryteria.")
    else:
        # st.success(f"Znaleziono {len(recommendations)} rekomendacje:")
        # st.dataframe(recommendations)
        recommendations = recommendations[list(selected_columns.keys())]

        # Zmiana nazw kolumn na polskie
        recommendations.rename(columns=selected_columns, inplace=True)

        # Wyświetlenie wyników z polskimi nazwami kolumn
        st.success(f"Znaleziono {len(recommendations)} rekomendacje:")
        st.dataframe(recommendations)
