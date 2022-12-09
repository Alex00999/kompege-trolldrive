from selenium import webdriver
import time
from selenium.webdriver.common.by import By

url_kompege_answers = 'https://kompege.ru/task'
url_kompege_course = 'https://kompege.ru/course'
url_vk_auth = 'https://oauth.vk.com/authorize?client_id=7631884&display=popup&redirect_uri=https://kompege.ru/auth' \
              '&response_type=code&v=5.131 '
driver = webdriver.Chrome(executable_path='chromedriver.exe')

LOGIN, PASSWORD = '', ''


def vk_login():
    driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[6]').send_keys(LOGIN)
    driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[7]').send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="install_allow"]').click()
    # time.sleep(100)


def find_ans(i):
    driver.refresh()
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/p[2]/input[1]').send_keys(i)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/p[2]/input[2]').click()
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/table/tr[2]/td[2]/span').click()
    answer = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/table/tr[2]/td[2]/p[2]').text
    if answer.split()[0] == 'Файлы':
        answer = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/table/tr[2]/td[2]/p[4]').text
    elif answer == 'Разбор':
        answer = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/table/tr[2]/td[2]/p[3]').text
    return answer


def fill_answers(module_amount):
    for n in range(2, module_amount + 3):
        print(f'Выполнено {n - 1} задание')
        # print(driver.find_elements(By.CLASS_NAME, 'block task-empty'))
        try:
            a = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[1]/div/div/div[{n}]')
        except:
            continue
        if a.get_attribute("class") == 'block task-good':
            continue
        a.click()
        try:
            task_number = driver.find_element(By.XPATH,
                                              '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div[2]/div/p/span').text
        except:
            print('В задании нет номера ответа')
            continue
        task_number = task_number.replace('(', '').replace(')', '').replace('№', '')
        driver.switch_to.window(driver.window_handles[-1])
        ans = find_ans(task_number)
        driver.switch_to.window(driver.window_handles[0])
        table_ex = [10, 27, 28, 29, 18, 26, 25, 24, 20]
        if (module - 3) in table_ex:
            k = driver.find_element(By.XPATH, '//*[@id="r0c0"]')
            j = driver.find_element(By.XPATH, '//*[@id="r0c1"]')
            k.clear()
            j.clear()
            ans_s = ans.split()
            k.send_keys(ans_s[0])
            j.send_keys(ans_s[1])
            driver.find_element(By.XPATH,
                                '//*[@id="app"]/div/div[2]/div/div/div/div[3]/div/div[2]/div[2]/input[2]').click()
            continue
        driver.find_element(By.CLASS_NAME, 'input').clear()
        driver.find_element(By.CLASS_NAME, 'input').send_keys(ans)
        try:
            driver.find_element(By.CLASS_NAME, 'save').click()
        except:
            print('Не смог сохранить')
            continue
        # print(task_number)
        # time.sleep(1)


try:
    driver.get(url=url_vk_auth)
    vk_login()
    time.sleep(1)
    driver.switch_to.new_window('tab')
    driver.get(url=url_kompege_answers)
    driver.switch_to.window(driver.window_handles[0])
    driver.get(url=url_kompege_course)
    driver.implicitly_wait(1)
    module = 3 + int(input('Введите модуль: '))
    for x in range(2, 6):
        z = driver.find_element(By.XPATH, f'//*[@id="app"]/div/nav/div/p[{module}]/ul/li[{x}]')
        # print(z.text.split()[0])
        if z.text.split()[0] != 'Домашняя':
            continue
        else:
            z.click()
            break
    new_module_amount = int(
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div[1]/div/div').text.split('\n')[-1])
    print('Кол-во заданий в модуле:', new_module_amount)
    if module - 3 in [8, 16]:
        fill_answers(new_module_amount)
        if module - 3 == 16:
            driver.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/p[19]/ul/li[4]').click()
        elif module - 3 == 8:
            driver.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/p[11]/ul/li[5]').click()
        fill_answers(20)
    else:
        fill_answers(new_module_amount)
    print('Завершение работы')
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
