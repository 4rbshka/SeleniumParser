from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

unique_questions = set()

with open('question.txt', 'r', encoding='utf-8') as file:
    for line in file:
        question_data = line.strip().split(';')
        question = question_data[0]
        correct_answer = question_data[1]
        unique_questions.add((question, correct_answer))

while True:
    try:
        # Инициализация драйвера
        driver = webdriver.Firefox()
        driver.get("https://selftest.mededtech.ru/")

        # код для ввода логина и пароля...
        login_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "j_username"))
        )
        login_input.send_keys("lylukvy@mailforspam.com")

        password_input = driver.find_element(By.NAME, "j_password")
        password_input.send_keys("12345")
        password_input.send_keys(Keys.RETURN)

        # создаём тест и заходим в него
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "dijit_form_Button_0_label"))).click()

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'extraSpace'))).click()

        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(5)
        driver.find_element(By.ID, 'xsltforms-subform-0-label-2_2_6_4_2_').click()

        # Завершаем его
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "xsltforms-subform-1-label-2_2_2_4_10_2_10_4_2_"))).click()

        time.sleep(3)
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.ID, "xsltforms-subform-1-label-2_2_4_2_10_2_10_4_2_"))).click()

        time.sleep(3)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "clonedId79"))).click()

        # Проходимся по вопросам и записываем их
        for step in range(80):
            time.sleep(4)
            correct_answer = driver.find_element(By.CSS_SELECTOR, '.correct_answer span.xforms-value p')
            elements = driver.find_elements(By.CSS_SELECTOR, 'span.xforms-value p')
            question = elements[0].text
            if (question, correct_answer.text) not in unique_questions:
                unique_questions.add((question, correct_answer.text))
                entry = [question, correct_answer.text] + [s.text for s in elements[1:] if
                                                           s.text != correct_answer.text]
                with open('question.txt', 'a', encoding='utf-8') as file:
                    for w in entry:
                        file.write(f'{w.strip()};')
                    file.write('\n')

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, f'xsltforms-subform-{step + 3}-label-2_2_2_4_2_10_4_2_'))
            ).click()

        # Закрываем браузер и начинаем заново
        driver.quit()
    except Exception as err:
        print(err)
        continue
    finally:
        driver.quit()