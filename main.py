from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from fuzzywuzzy import process

def similarity_2(list, string):
    best_match, confidence = process.extractOne(string, list)
    return confidence

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

data = {'company': [], 'title': [], 'zps': [], 'link': [], 'reqs': []}
key_words = ['требования', 'идеальный кандидат', 'для нас важно что', 'Что нужно, чтобы к нам '
                                                                                'присоединиться',
        'Для этой работы нам нужен именно такой как ты', 'Что мы ценим', 'Что мы ждем', 'Нам нужен коллега с', 'Необходимые навыки и умения', 'Ожидаем']

for i in range(1):
    driver.get(
        f'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&only_with_salary=true&text=%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%BE%D0%B2%D1%8B%D0%B9+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA&page={i}')
    print('Site has loaded')
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    company = driver.find_elements(By.CLASS_NAME, 'vacancy-serp-item__meta-info-company')
    print('companies parsed')
    time.sleep(2)
    zps = driver.find_elements(By.CSS_SELECTOR, 'span.bloko-header-section-3')
    print('zps parsed')
    time.sleep(1.4)
    title = driver.find_elements(By.CSS_SELECTOR, 'h3.bloko-header-section-3')
    print('titles parsed')
    time.sleep(2.3)
    link = driver.find_elements(By.CLASS_NAME, 'serp-item__title')
    print('links parsed')
    time.sleep(1.5)
    for j in range(len(company)):
        data['company'].append(company[j].text)
        data['zps'].append(zps[j].text.replace(u"\u202f", " "))
        data['title'].append(title[j].text)
        data['link'].append(link[j].get_attribute('href'))
    time.sleep(1)
for key in data:
    print(len(data[key]))

for i, link in enumerate(data['link']):
    print(f'{i}. Ссылка: {data["link"][i]}')
    flag = False
    driver.get(link)
    time.sleep(4)
    strongs = driver.find_elements(By.TAG_NAME, 'strong')
    for strong in strongs:
        if similarity_2(key_words, strong.text) > 69 and not flag:
            try:
                flag = True
                req_xpath = f'//strong/span[text()="{strong.text}"]//..//..//following-sibling::ul'
                data['reqs'].append(driver.find_element(By.XPATH, req_xpath).text.replace('\n', '// '))
            except NoSuchElementException:
                flag = True
                data['reqs'].append(None)
                print(f'Причина: Не найден абзац с названием {strong.text}')
            except SyntaxError:
                flag = True
                data['reqs'].append(None)
                print(f'Этот сайт поебень')
    if not flag:
        data['reqs'].append(None)
        print('Причина: Не найдено подходящее название для абзаца')
    print(data['reqs'][i])


print(len(data['reqs']))

with open('data.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    df = pd.DataFrame.from_dict(data=data)
    print(df)
    df.to_csv(f)


driver.quit()
