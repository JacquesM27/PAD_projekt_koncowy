import re
import time

import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver

from common.file_utils import read_last_size_from_file, save_last_size_to_file
from models.TyreModels import TyreSizeData


def scrap_sklep_opon(driver: WebDriver):
    sklep_opon_base_url = "https://www.sklepopon.com/szukaj-opony?sezon=letnie&rozmiar={}&ofs="
    last_size_file_path = "data/sklep_opon/tmp/last_size.txt"

    last_size = read_last_size_from_file(last_size_file_path)
    start_index = 0

    if last_size:
        for i, size in enumerate(TyreSizeData.SIZES):
            if str(size) == last_size:
                start_index = i + 1
                break
    else:
        start_index = 0

    for tyre_size in TyreSizeData.TYRE_DATA[start_index:]:
        print(f"Scrapowanie danych dla rozmiaru: {tyre_size}")
        sklep_opon_tires_data = []
        offset = 0

        while True:
            url = sklep_opon_base_url.format(tyre_size) + str(offset)
            print(f"Otwieranie URL: {url}")
            driver.get(url)
            time.sleep(4)

            if offset == 0:
                close_sklep_opon_popups(driver)

            tires_data = load_sklep_opon_tire_data(driver)
            sklep_opon_tires_data.extend(tires_data)

            offset += 20
            # Sprawdzenie końca paginacji
            if len(driver.find_elements(By.CSS_SELECTOR, 'div[data-c-name="listing-products-element"]')) == 0:
                print(f"Brak nowych danych dla rozmiaru: {tyre_size}. Koniec paginacji.")
                break

        # Zapis danych do CSV z poprawną nazwą pliku
        safe_filename = tyre_size.to_safe_filename()
        csv_file = f"data/sklep_opon/sklep_opon_{safe_filename}.csv"
        df = pd.DataFrame(sklep_opon_tires_data)
        df.to_csv(csv_file, index=False)
        print(f"Zapisano dane do pliku: {csv_file}")

        # Zapis ostatniego rozmiaru do pliku
        save_last_size_to_file(str(tyre_size), last_size_file_path)

    print("Proces scrapowania zakończony.")


def close_sklep_opon_popups(driver: WebDriver):
    try:
        btn_cookie = driver.find_element(By.CSS_SELECTOR, "#klaro > div > div > div > div > div > button")
        btn_cookie.click()
        print("Przycisk akceptacji ciasteczek został kliknięty.")
    except NoSuchElementException:
        print("Przycisk akceptacji ciasteczek nie został znaleziony.")
    except Exception as exception:
        print("Nie udało się kliknąć przycisku akceptacji ciasteczek:", exception)

    try:
        driver.execute_script("""
            const shadowHost = document.querySelector("body > div.gr-visual-prompt");
            if (shadowHost) {
                const shadowRoot = shadowHost.shadowRoot;
                const closeButton = shadowRoot.querySelector("div > div:nth-child(2) > button:nth-child(1)");
                if (closeButton) {
                    closeButton.click();
                    console.log("Okienko powiadomień zostało zamknięte.");
                } else {
                    console.log("Nie znaleziono przycisku zamknięcia powiadomień.");
                }
            } else {
                console.log("Okno powiadomień nie zostało znalezione.");
            }
        """)
    except Exception as exception:
        print("Nie udało się zamknąć okienka powiadomień:", exception)


def load_sklep_opon_tire_data(driver: WebDriver):
    scrapped_data = []
    try:
        tire_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-c-name="listing-products-element"]')

        class_mapping = {
            "Premium": "Premium",
            "Średnia": "Średnia",
            "Średniej": "Średnia",
            "Ekonomiczna": "Ekonomiczna",
            "Ekonomicznej": "Ekonomiczna"
        }

        for tire_element in tire_elements:

            try:
                load_index = tire_element.find_element(By.CSS_SELECTOR, 'li[data-attribute-code="li"]').text
                speed_index = tire_element.find_element(By.CSS_SELECTOR, 'li[data-attribute-code="si"]').text
            except NoSuchElementException:
                load_index = None
                speed_index = None

            noise_level = None
            try:
                noise_level_elements = tire_element.find_elements(By.CSS_SELECTOR,
                                                                  "span.self-center.tracking-tighter.sm\\:tracking-normal")
                for noise_level_element in noise_level_elements:
                    text = noise_level_element.text
                    match = re.search(r'\d+', text)
                    if match:
                        noise_level = int(match.group())
            except (NoSuchElementException, IndexError):
                pass

            etykieta_elements = tire_element.find_elements(By.CSS_SELECTOR,
                                                           'span.icon-fuel-new ~ span, span.icon-rain-new ~ span, span.icon-speaker-new ~ span')
            fuel_index = etykieta_elements[0].text if len(etykieta_elements) > 0 else None
            wet_grip_index = etykieta_elements[1].text if len(etykieta_elements) > 1 else None
            noise_index = etykieta_elements[2].text.split(" ")[0] if len(etykieta_elements) > 2 else None

            try:
                tire_class_element = tire_element.find_element(By.XPATH,
                                                               ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'klas')]")
                tire_class_text = tire_class_element.text.lower().replace("w klasie ", "").replace("klasa ",
                                                                                                   "").strip().capitalize()
                tire_class = class_mapping.get(tire_class_text, tire_class_text)
            except NoSuchElementException:
                tire_class = None

            try:
                user_rating_element = tire_element.find_element(By.XPATH,
                                                                ".//li[contains(@class, 'xl:hidden')]//span[contains(@class, 'ml-1')]")
                user_rating = float(user_rating_element.text.replace(",", "."))
            except NoSuchElementException:
                user_rating = None

            price = float(tire_element.get_attribute('data-ee-product-properties').split(";")[3].split(":")[1])

            try:
                availability_element = tire_element.find_element(By.CSS_SELECTOR, "div.tooltip-product-listing")
                availability_code = availability_element.get_attribute("data-attribute-code")

                if availability_code == "item_availability_tooltip_high":
                    availability = "full"
                elif availability_code == "item_availability_tooltip_medium":
                    availability = "medium"
                elif availability_code == "item_availability_tooltip_low":
                    availability = "low"
                elif availability_code == "item_availability_tooltip_last":
                    availability = "last"
                else:
                    availability = None
            except NoSuchElementException:
                availability = None

            tire_data = {
                "name": tire_element.get_attribute("data-ee-product-properties").split(";")[0].split(":")[1],
                "brand": tire_element.get_attribute("data-ee-product-properties").split(";")[4].split(":")[1],
                "model": tire_element.get_attribute("data-ee-product-properties").split(";")[6].split(":")[1],
                "size": tire_element.get_attribute("data-ee-product-properties").split(";")[5].split(":")[1],
                "load_index": load_index,
                "speed_index": speed_index,
                "fuel_index": fuel_index,
                "wet_grip_index": wet_grip_index,
                "noise_index": noise_index,
                "noise_level": noise_level,
                "class": tire_class,
                "user_rating": user_rating,
                "price": price,
                "availability": availability
            }

            scrapped_data.append(tire_data)
    finally:
        pass
    return scrapped_data