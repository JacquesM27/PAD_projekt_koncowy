import json
import time
import re

import pandas as pd
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from common.file_utils import read_last_size_from_file, save_last_size_to_file
from models.TyreModels import TyreSizeData


def scrap_oponeo(driver):
    last_size = read_last_size_from_file("data/oponeo/tmp/last_size.txt")
    start_index = 0

    if last_size:
        for i, size in enumerate(TyreSizeData.SIZES):
            if str(size) == last_size:
                start_index = i + 1
                break
    else:
        start_index = 0

    # Główna pętla
    for tyre_size in TyreSizeData.TYRE_DATA[start_index:]:
        size_str = str(tyre_size)
        print(f"Rozpoczynam scrapowanie dla rozmiaru: {size_str}")
        oponeo_base_url = f"https://www.oponeo.pl/wybierz-opony/s=1/letnie/t=1/osobowe/r=1/{tyre_size.width}-{tyre_size.profile}-r{tyre_size.diameter}"

        # otworzenie drivera jeszcze raz
        driver.close()
        download_service = Service()
        driver = webdriver.Chrome(service=download_service)
        driver.set_window_size(1100, 800)
        driver.get(oponeo_base_url)
        close_oponeo_popup(driver)

        oponeo_tires_data = []
        page_number = 1
        time.sleep(3)
        while True:
            tires_data = load_oponeo_tire_data(driver)
            oponeo_tires_data.extend(tires_data)

            page_number += 1
            if not load_next_oponeo_page(driver, page_number):
                print("Brak nowych danych. Koniec paginacji.")
                break

        # Zapis do pliku CSV
        csv_filename = f"data/oponeo/oponeo_{tyre_size.width}_{tyre_size.profile}_{tyre_size.diameter}.csv"
        df = pd.DataFrame(oponeo_tires_data)
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"Dane zapisano do pliku: {csv_filename}")

        # Zapis ostatniego rozmiaru
        save_last_size_to_file(size_str, "data/oponeo/tmp/last_size.txt")
        print(f"Zapisano ostatni rozmiar: {size_str}")

    print("Scrapowanie oponeo zakończone.")

def close_oponeo_popup(driver):
    try:
        reject_button = driver.find_element(By.CSS_SELECTOR, "#consentsBar > div.buttonsContainer.container > div > span.reject")
        reject_button.click()
        print("Okienko prywatności zostało zamknięte.")
    except NoSuchElementException:
        print("Okienko prywatności nie jest widoczne lub zostało już zamknięte.")
    except Exception as e:
        print("Wystąpił błąd podczas zamykania okienka prywatności:", e)

def load_next_oponeo_page(driver, current_page_number):
    try:
        next_page_button = driver.find_element(By.ID, f"_ctPgrp_pi{current_page_number}i")
        next_page_button.click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        return False


def load_oponeo_tire_data(driver):
    scrapped_data = []
    tire_elements = driver.find_elements(By.CLASS_NAME, "product")  # Wszystkie produkty na stronie

    for tire_element in tire_elements:
        try:
            # Pobieranie danych z `data-layer`
            try:
                data_layer = tire_element.get_attribute("data-layer")
                product_data = json.loads(data_layer) if data_layer else {}
            except json.JSONDecodeError:
                product_data = {}

            # Pobieranie nazwy
            name = product_data.get("item_name")  # Z `data-layer`

            # Pobieranie producenta
            brand = product_data.get("item_brand")  # Z `data-layer`

            # Pobieranie klasy opony
            tire_class = product_data.get("item_category4", "").replace("Klasa ", "").capitalize()

            # Pobieranie ceny
            try:
                price = product_data.get("price") or tire_element.find_element(By.CLASS_NAME, "priceValue").text
            except NoSuchElementException:
                price = None

            # Pobieranie modelu
            try:
                model = tire_element.find_element(By.CLASS_NAME, "modelName").text
            except NoSuchElementException:
                model = None

            # Pobieranie rozmiaru
            try:
                size = tire_element.find_element(By.CLASS_NAME, "modelSize").text
            except NoSuchElementException:
                size = None

            # Pobieranie indeksu nośności
            try:
                load_index = tire_element.find_element(By.CSS_SELECTOR, ".extra[data-tp='TireLoadIndex'] em").text
            except NoSuchElementException:
                load_index = None

            # Pobieranie indeksu prędkości
            try:
                speed_index = tire_element.find_element(By.CSS_SELECTOR, ".extra[data-tp='TireSpeedIndex'] em").text
            except NoSuchElementException:
                speed_index = None

            # Pobieranie wskaźników efektywności (paliwo, deszcz, hałas)
            try:
                fuel_index = tire_element.find_element(By.CSS_SELECTOR, ".icon-fuel em").text
            except NoSuchElementException:
                fuel_index = None

            try:
                wet_grip_index = tire_element.find_element(By.CSS_SELECTOR, ".icon-rain em").text
            except NoSuchElementException:
                wet_grip_index = None

            # Pobieranie wskaźnika hałasu
            try:
                noise_element = tire_element.find_element(By.CSS_SELECTOR, ".icon-noise em").text
                noise_match = re.match(r"([A-E])\s*(\d+)", noise_element)
                noise_index = noise_match.group(1) if noise_match else None
                noise_level = int(noise_match.group(2)) if noise_match else None
            except NoSuchElementException:
                noise_index = None
                noise_level = None

            # Pobieranie oceny użytkowników
            try:
                user_rating = tire_element.find_element(By.CSS_SELECTOR, ".productRating .note").text.replace(",", ".")
            except NoSuchElementException:
                user_rating = None

            # Pobieranie dostępności
            try:
                stock_level_element = tire_element.find_element(By.CSS_SELECTOR, ".stockLevel")
                stock_level_class = stock_level_element.get_attribute("class").split()[-1]

                if stock_level_class == "full":
                    availability = "full"
                elif stock_level_class == "medium":
                    availability = "medium"
                elif stock_level_class == "low":
                    availability = "low"
                else:
                    availability = "unknown"
            except NoSuchElementException:
                availability = "unknown"

            # Tworzenie obiektu opony
            tire_info = {
                "name": name,
                "brand": brand,
                "model": model,
                "size": size,
                "load_index": load_index,
                "speed_index": speed_index,
                "fuel_index": fuel_index,
                "wet_grip_index": wet_grip_index,
                "noise_index": noise_index,
                "noise_level": noise_level,
                "class": tire_class,
                "user_rating": user_rating,
                "price": price,
                "availability": availability,
            }

            scrapped_data.append(tire_info)

        except Exception as e:
            print(f"Error processing tire: {e}")
            continue

    return scrapped_data