import os

import pandas as pd


# Funkcja zapisująca aktualny rozmiar do pliku
def save_last_size_to_file(size_tyre, path):
    with open(path, "w") as file:
        file.write(size_tyre)
    print(f"Zapisano aktualny rozmiar: {size_tyre}")

# Funkcja odczytująca ostatni zapisany rozmiar
def read_last_size_from_file(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            return file.read().strip()
    return None


def load_dataframe_from_csv_files(directory):
    # Lista do przechowywania DataFrame'ów
    dataframes = []

    # Iteracja po plikach w katalogu
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):  # Sprawdzamy tylko pliki CSV
            file_path = os.path.join(directory, filename)
            print(f"Ładowanie pliku: {file_path}")

            # Sprawdzenie, czy plik nie jest pusty
            if os.path.getsize(file_path) > 0:
                try:
                    tmp_df = pd.read_csv(file_path)
                    dataframes.append(tmp_df)
                except Exception as e:
                    print(f"Błąd podczas wczytywania pliku {file_path}: {e}")
            else:
                print(f"Plik {file_path} jest pusty i został pominięty.")

    # Łączenie wszystkich DataFrame'ów w jeden
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        print(f"Połączono {len(dataframes)} plików CSV.")
        return merged_df
    else:
        print("Brak plików CSV do połączenia.")
        return pd.DataFrame()