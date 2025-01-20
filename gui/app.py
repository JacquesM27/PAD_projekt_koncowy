import os
import sys
import streamlit as st
import pandas as pd
import pickle

# Dodanie katalogu głównego projektu do ścieżki, żeby ładować dane i modele
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Wczytaj dane i modele
def load_data_and_models():
    with open('data/models/price_prediction_model.pkl', 'rb') as f:
        price_model = pickle.load(f)
    with open('data/models/tyres_model.pkl', 'rb') as f:
        recommendation_model = pickle.load(f)
    with open('data/models/tyres_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    tyre_data = pd.read_csv('data/models/tyres_data.csv')
    return price_model, recommendation_model, scaler, tyre_data


# Wczytaj modele i dane
price_model, recommendation_model, scaler, df = load_data_and_models()
df = df.dropna()

# Interfejs aplikacji
st.title("Aplikacja do przewidywania i rekomendacji opon")
menu = st.sidebar.radio("Wybierz opcję", ["Przewidywanie ceny", "Rekomendacje opon", "Wyszukiwarka opon"])

# Zakładka 1: Przewidywanie ceny
if menu == "Przewidywanie ceny":
    st.header("Przewidywanie ceny opony")
    brands = sorted(df['brand'].dropna().unique())
    retailers = sorted(df['retailer'].dropna().unique())
    sizes = sorted(df['size'].dropna().unique())
    classes = sorted(df['class'].dropna().unique())
    load_indices = sorted(df['load_index'].dropna().unique())
    fuel_indices = ['A', 'B', 'C', 'D', 'E']
    wet_grip_indices = ['A', 'B', 'C', 'D', 'E']
    noise_indices = ['A', 'B', 'C']

    brand = st.selectbox("Marka:", options=brands)
    retailer = st.selectbox("Sprzedawca:", options=retailers)
    size = st.selectbox("Rozmiar (np. 205/55 R16):", options=sizes)
    tyre_class = st.selectbox("Klasa:", options=classes)
    load_index = st.selectbox("Indeks nośności:", options=load_indices)
    fuel_index = st.selectbox("Indeks paliwowy:", options=fuel_indices)
    wet_grip_index = st.selectbox("Indeks na mokrej nawierzchni:", options=wet_grip_indices)
    noise_index = st.selectbox("Indeks hałasu:", options=noise_indices)

    if st.button("Przewiduj cenę"):
        input_data = pd.DataFrame({
            'brand': [brand],
            'retailer': [retailer],
            'size': [size],
            'class': [tyre_class],
            'load_index': [load_index],
            'fuel_index': [fuel_index],
            'wet_grip_index': [wet_grip_index],
            'noise_index': [noise_index]
        })
        try:
            predicted_price = price_model.predict(input_data)[0]
            st.success(f"Przewidywana cena opony: {predicted_price:.2f} PLN")
        except Exception as e:
            st.error(f"Błąd podczas przewidywania: {e}")

# Zakładka 2: Rekomendacje opon
elif menu == "Rekomendacje opon":
    st.header("Rekomendacje opon")
    max_price = st.number_input("Maksymalna cena (PLN):", min_value=0.0, value=500.0, step=1.0)
    max_user_rating = df['user_rating'].max()
    min_rating = st.slider("Minimalna ocena użytkownika:", min_value=1.0, max_value=max_user_rating, step=0.1,
                           value=4.0)
    available_sizes = sorted(df['size'].unique())
    selected_size = st.selectbox("Rozmiar opony (np. 205/55 R16):", available_sizes)
    selected_class = st.selectbox("Klasa opony:", options=[""] + list(df['class'].unique()))
    brand = st.text_input("Preferowana marka (opcjonalnie):")

    if st.button("Rekomenduj"):
        filtered_df = df[
            (df['price'] <= max_price) &
            (df['user_rating'] >= min_rating) &
            (df['size'] == selected_size)
            ]
        if brand:
            filtered_df = filtered_df[filtered_df['brand'] == brand]
        if selected_class:
            filtered_df = filtered_df[filtered_df['class'] == selected_class]

        if filtered_df.empty:
            st.warning("Brak wyników spełniających kryteria. Wyświetlam najlepsze ogólne wyniki.")
            filtered_df = df.copy()

        X_filtered = filtered_df[['price', 'user_rating', 'noise_index_numeric',
                                  'wet_grip_index_numeric', 'fuel_index_numeric', 'speed_index_numeric']]
        X_filtered_scaled = scaler.transform(X_filtered)
        predictions = recommendation_model.predict(X_filtered_scaled)
        filtered_df['predicted_score'] = predictions
        top_n = 3
        recommendations = filtered_df.sort_values(by='predicted_score', ascending=False).head(top_n)
        st.dataframe(recommendations)

# Zakładka 3: Wyszukiwarka opon (po modyfikacji - dodanie modelu dynamicznie)
elif menu == "Wyszukiwarka opon":
    st.header("Wyszukiwarka opon z pliku CSV")

    # Wybór parametrów
    brands = sorted(df['brand'].dropna().unique())
    retailers = sorted(df['retailer'].dropna().unique())
    sizes = sorted(df['size'].dropna().unique())
    classes = sorted(df['class'].dropna().unique())
    load_indices = sorted(df['load_index'].dropna().unique())
    fuel_indices = ['A', 'B', 'C', 'D', 'E']
    wet_grip_indices = ['A', 'B', 'C', 'D', 'E']
    noise_indices = ['A', 'B', 'C']

    # Wybór parametrów użytkownika
    max_price = st.number_input("Maksymalna cena (PLN):", min_value=0.0, value=500.0, step=1.0)
    brand = st.selectbox("Marka:", options=[""] + brands)
    # Dynamiczne ładowanie modeli na podstawie wybranej marki
    models = sorted(df[df['brand'] == brand]['model'].dropna().unique()) if brand else []
    model = st.selectbox("Model:", options=[""] + models)

    retailer = st.selectbox("Sprzedawca:", options=[""] + retailers)
    size = st.selectbox("Rozmiar (np. 205/55 R16):", options=[""] + sizes)
    tyre_class = st.selectbox("Klasa opony:", options=[""] + classes)
    load_index = st.selectbox("Indeks nośności:", options=[""] + load_indices)
    fuel_index = st.selectbox("Indeks paliwowy:", options=[""] + fuel_indices)
    wet_grip_index = st.selectbox("Indeks na mokrej nawierzchni:", options=[""] + wet_grip_indices)
    noise_index = st.selectbox("Indeks hałasu:", options=[""] + noise_indices)

    if st.button("Szukaj"):
        # Filtrowanie danych na podstawie wybranych parametrów
        search_results = df[
            (df['price'] <= max_price) &
            (df['brand'] == brand if brand else True) &
            (df['model'] == model if model else True) &
            (df['retailer'] == retailer if retailer else True) &
            (df['size'] == size if size else True) &
            (df['class'] == tyre_class if tyre_class else True) &
            (df['load_index'] == load_index if load_index else True) &
            (df['fuel_index'] == fuel_index if fuel_index else True) &
            (df['wet_grip_index'] == wet_grip_index if wet_grip_index else True) &
            (df['noise_index'] == noise_index if noise_index else True)
            ]

        if search_results.empty:
            st.warning("Brak wyników spełniających kryteria.")
        else:
            st.success("Znalezione wyniki:")
            # Usuwamy kolumnę 'name' i wyświetlamy resztę wyników
            search_results = search_results.drop(columns=["name"], errors="ignore")
            st.dataframe(search_results)
