from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def check_and_handle_captcha(driver):

    try:
        # Проверяем различные виды капчи
        captcha_selectors = [
            "iframe[src*='captcha']",
            "iframe[src*='recaptcha']",
            "div.captcha",
            "div.recaptcha",
            "div#captcha",
            "div#recaptcha",
        ]

        for selector in captcha_selectors:
            captcha_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if captcha_elements:
                print("Обнаружена капча! Пытаемся обработать...")

                # Даем время пользователю решить капчу вручную
                print("Решите капчу в браузере в течение 30 секунд...")
                time.sleep(30)

                # Проверяем, исчезла ли капча
                captcha_elements_after = driver.find_elements(By.CSS_SELECTOR, selector)
                if not captcha_elements_after:
                    print("Капча решена, продолжаем тест")
                    return True
                else:
                    print("Капча не решена, делаем скриншот")
                    driver.save_screenshot("captcha_error.png")
                    return False

    except Exception as e:
        print(f"Ошибка при проверке капчи: {e}")

    return True


def test_google():
    print("Запускаем тест Google")

    # Автоматически скачиваем и настраиваем ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Главная страница
        print("1. Переходим на google.com")
        driver.get("https://www.google.com")

        # Ждем загрузки страницы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        time.sleep(2)

        # Проверяем заголовок
        print("2. Проверяем заголовок страницы")
        if "Google" not in driver.title:
            raise Exception("Заголовок не содержит 'Google'")
        print("Заголовок корректен!")

        # Находим поисковую строку и вводим запрос
        print("3. Вводим поисковый запрос")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium автоматическое тестирование")
        search_box.send_keys(Keys.RETURN)

        # Ждем результаты поиска
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        time.sleep(2)

        # Проверяем результаты
        print("4. Проверяем результаты поиска")
        if "Selenium" not in driver.title:
            raise Exception("Поиск не сработал")
        print(" Поиск выполнен успешно!")

        # Проверяем наличие результатов
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        print(f" Найдено {len(results)} результатов поиска")

        print("\n ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")

    except Exception as e:
        print(f" ОШИБКА: {e}")
        # Делаем скриншот при ошибке
        driver.save_screenshot("error_screenshot.png")
        print("Скриншот ошибки сохранен как 'error_screenshot.png'")
    finally:
        # Закрываем браузер
        driver.quit()
        print("Браузер закрыт")


# Запускаем тест
if __name__ == "__main__":
    test_google()
