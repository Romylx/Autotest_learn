from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os


def take_screenshot(driver, test_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Скриншот сохранен: {filename}")
    return filename


def test_yandex_travel_search():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        driver.get("https://yandex.ru")

        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "text"))
        )

        search_text = "достопримечательности санкт-петербурга"
        for char in search_text:
            search_box.send_keys(char)
            time.sleep(0.1)

        time.sleep(1)
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.serp-item"))
        )

        first_link = driver.find_element(By.CSS_SELECTOR, "li.serp-item a.Link")
        first_link.click()

        time.sleep(3)

        driver.back()

        time.sleep(2)

        places_tab = driver.find_element(By.CSS_SELECTOR, "a[data-id='maps']")
        places_tab.click()

        time.sleep(3)

        print("Поиск достопримечательностей выполнен")

    except Exception as e:
        print(f"Ошибка: {e}")
        take_screenshot(driver, "yandex_error")
    finally:
        driver.quit()


def test_wikipedia_culture():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        driver.get("https://ru.wikipedia.org")

        search_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )

        search_text = "эрмитаж музей"
        for char in search_text:
            search_input.send_keys(char)
            time.sleep(0.1)

        time.sleep(1)
        search_button = driver.find_element(By.ID, "searchButton")
        search_button.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "firstHeading"))
        )

        content = driver.find_element(By.ID, "bodyContent")
        if content.is_displayed():
            print("Статья найдена и отображается")

        time.sleep(2)

    except Exception as e:
        print(f"Ошибка: {e}")
        take_screenshot(driver, "wikipedia_error")
    finally:
        driver.quit()


def test_avito_search():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        driver.get("https://www.avito.ru")

        search_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-marker='search-form/suggest']")
            )
        )

        search_text = "велосипед"
        for char in search_text:
            search_input.send_keys(char)
            time.sleep(0.1)

        time.sleep(1)
        search_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-marker='search-form/submit-button']"
        )
        search_button.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-marker='item']"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        if len(items) > 0:
            print(f"Найдено {len(items)} товаров")

        time.sleep(2)

    except Exception as e:
        print(f"Ошибка: {e}")
        take_screenshot(driver, "avito_error")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_yandex_travel_search()
    test_wikipedia_culture()
    test_avito_search()
