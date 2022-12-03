import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.notebook import tqdm
import time
import numpy as np
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


def extract_links(driver: selenium.webdriver, jobs_number: int):
    """
    Функция достает все ссылки ведущие на страницы вакансий.

    :param driver: selenium.webdriver
    :param jobs_number: int количество вакансий
    :return: list ссылки ведущие на страницы вакансий
    """
    # список ссылок на вакансии
    all_links = []

    # номер страницы
    page = 1

    while len(all_links) < jobs_number:
        # селектор кнопки следующей страницы на 1 страницу
        next_page_selector = '#jobsearch-JapanPage > div > div > div.jobsearch-SerpMainContent >' \
                             ' div.jobsearch-LeftPane > nav > div:nth-child(6) > a'
        if page > 1:
            # селектор кнопки следующей страницы на следующих страницах
            next_page_selector = '#jobsearch-JapanPage > div > div > div.jobsearch-SerpMainContent >' \
                                 ' div.jobsearch-LeftPane > nav > div:nth-child(7) > a'
        # все элементы страницы, содержащие ссылки
        elements = driver.find_elements(By.XPATH, "//a[@href]")
        # достанем ссылки из каждого элемента
        for elem in elements:
            link = elem.get_attribute("href")
            # ссылки открывающие вакансии на новой странице содержат в себе 'clk?jk'
            if 'clk?jk' in link:
                # добавляем ссылку в списо ссылок
                all_links.append(link)
        # собрав все ссылки на вакансии, переходим на следующую страницу
        next_page = driver.find_element(By.CSS_SELECTOR,
                                        next_page_selector)
        next_page.click()
        page += 1
        # рандомное количество секунд сна
        sleep = np.random.choice([3, 7, 9, 13, 15, 19])
        time.sleep(sleep)

    return all_links


def extract_web_pages(driver: selenium.webdriver, links: list):
    """
    Функция сохраняет web-страницы, на которые ведут ссылки.

    :param driver: selenium.webdriver
    :param links: list ссылок, по которым нужно пройтись
    :return: list web-страниц
    """
    all_pages = []

    for link in tqdm(links):
        try:
            # переходим на страницу вакансии
            driver.get(link)
            # рандомное количество секунд сна
            sleep = np.random.choice([2, 3, 4])
            time.sleep(sleep)
            # фиксируем страницу
            page = driver.page_source
            # сохраняем страницу
            all_pages.append(page)
        except:
            print('Не удалось выгрузить html-страницу')
            continue

    return all_pages


def parse_ds_jobs(location: str, jobs_number: int):
    """
    Функция парсит сайт indeed.com и достает страницы с вакансиями data scientist
    с годовой компенсацией выше $50,000.

    :param location: str штат/город поиска вакансий
    :param jobs_number: int количество вакансий, которое нужно спарсить
    :return:
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Заходим на 1 страницу поиска

    # открываем страницу
    driver.get("https://www.indeed.com/")
    time.sleep(3)
    # текст поиска
    job = 'data scientist $50,000'

    # поле job title
    job_title_search_field = driver.find_element(By.CSS_SELECTOR,
                                                 '#text-input-what')
    time.sleep(3)
    # ввод запроса в поле job title
    job_title_search_field.send_keys(job)
    driver.implicitly_wait(3)

    # поле location
    location_search_field = driver.find_element(By.CSS_SELECTOR,
                                                '#text-input-where')
    time.sleep(3)
    # ввод запроса в поле location
    location_search_field.send_keys(location)
    driver.implicitly_wait(2)

    # кнопка поиска
    search_button = driver.find_element(By.CSS_SELECTOR,
                                        '#jobsearch > button')
    time.sleep(1)
    # нажимаем на кнопку поиска
    search_button.click()

    # Извлечение ссылок на вакансии
    all_links = extract_links(driver=driver, jobs_number=jobs_number)

    # Извлечение web-cтраниц вакансий
    all_jobs = extract_web_pages(driver=driver, links=all_links)

    return all_jobs


def save_web_pages(pages: list, path: str):
    """
    Функция сохраняет web-страницы в указанную директорию.

    :param pages: list web-страниц
    :param path: str директория для сохранения
    """
    for idx, page in enumerate(pages):
        page = bs(page, 'html')
        with open(path + f"_{idx}.html", "w") as file:
            file.write(str(page))


def read_web_pages(path: str, pages_num: int):
    """
    Функция извлекает web-страницы из указанного пути.

    :param path: str путь к директории с web-страницами
    :param pages_num: int число web-страниц в директории
    :return: list web-страниц
    """
    pages = []
    for idx in range(pages_num):
        with open(path + f"_{idx}.html", "r") as file:
            page = bs(file.read(), 'html')
            pages.append(page)

    return pages


def extract_data(path: str, num_pages: int, state: str):
    """
    Функция собирает информацию из сохраненных страниц
    и создает из нее датафрейм.

    :param path: str путь до директории с web-страницами
    :param num_pages: int количество вакансий
    :param state: str штат, в котором собирались вакансии
    :return: pd.DataFrame
    """
    job_titles = []
    companies = []
    apply_links = []
    companies_accounts = []
    descriptions = []
    salaries = []
    estimated_salaries = []
    all_benefits = []
    locations = []
    levels = []

    for i in range(num_pages):
        with open(f"{path}{i}.html", "r") as file:
            soup = bs(file.read(), 'html')
            # название вакансии
            try:
                job_title = soup.find('h1',
                                      {'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
                job_titles.append(job_title)
            except:
                job_titles.append(np.nan)
            #  название компании
            try:
                company = soup.find('div',
                                    {'class': 'jobsearch-CompanyInfoContainer'}).a.text
                companies.append(company)
            except:
                companies.append(np.nan)
            try:
                apply_link = soup.find('div', {'id': 'applyButtonLinkContainer'}).a['href']
                apply_links.append(apply_link)
            except:
                apply_links.append(np.nan)
            # страницы компаний на indeed
            try:
                company_account = soup.find('div',
                                            {'class': 'jobsearch-CompanyInfoContainer'}).a['href']
                companies_accounts.append(company_account)
            except:
                companies_accounts.append(np.nan)
            # описание вакансий
            try:
                full_desc = full_desc = soup.find_all('div', {'id': 'jobDescriptionText'})[0].text
                descriptions.append(full_desc)
            except:
                descriptions.append(np.nan)
            # зп если указано
            try:
                salary = soup.find('span', {'class': 'icl-u-xs-mr--xs'}).text
                salary = salary.replace(',', '')
                salary = [i for i in map(int, re.findall('[0-9]+', salary))]
                salaries.append(salary)
            except:
                salaries.append(np.nan)
            # оценочная зп
            try:
                estimated_salary = soup.find('div', {'id': 'salaryGuide'}).text
                estimated_salary = [i * 1000 for i in map(float, re.findall('(?:\d*\.\d+|\d+)', estimated_salary))]
                estimated_salaries.append(estimated_salary)
            except:
                estimated_salaries.append(np.nan)
            # benefits
            try:
                benefits = soup.find_all('div', {'class': 'css-1f2yqp0 e1xnxm2i0'})
                benefits = [i.text for i in benefits]
                all_benefits.append(benefits)
            except:
                all_benefits.append(np.nan)
            # locations
            try:
                location = soup.find_all('div', {'class': 'jobsearch-RelatedLinks-linkWrapper'})[0]
                location = ' '.join(location.text.split(' ')[-3:])
                location = ' '.join(re.findall('([A-Z][a-z0-9]+)+', location))
                locations.append(location)
            except:
                locations.append(np.nan)
            # уровень должности
            try:
                level = soup.find_all('div', {'class': 'jobsearch-RelatedLinks-linkWrapper'})[2]

                level = level.text.split(' ')[0]
                levels.append(level)
            except:
                levels.append(np.nan)
    # создадим датафрейм
    data = pd.DataFrame(
        {
            'title': job_titles,
            'company': companies,
            'apply_link': apply_links,
            'company_account': companies_accounts,
            'compensation': salaries,
            'est. compensation': estimated_salaries,
            'benefits': all_benefits,
            'location': locations,
            'level': levels,
            'description': descriptions
        }
    )
    # вакансии, в которых не указана зп, заполним оценкой indeed.com по этому району
    data['compensation'] = data['compensation'].fillna(data['est. compensation'])
    data.drop('est. compensation', axis=1, inplace=True)
    # в большинстве вакансий зп указана в формато ОТ - До -, заменим эти значения на среднее
    data['compensation'] = data['compensation'].apply(lambda x: np.array(x).mean())
    # если зп меньше ~300, значит зп указана за часы => умножим это значение на количество рабочих часов в году
    data.loc[data['compensation'] < 500, 'compensation'] = data['compensation'] * 2080
    # если зп меньше ~20000, значит зп указана за месяц => умножим это значение на количество месяцев в году
    data.loc[data['compensation'] < 20000, 'compensation'] = data['compensation'] * 12
    data['state'] = state
    # уровни должности
    title_levels = ['Senior', 'Principal', 'Lead', 'Director', 'Head', 'Junior', 'Staff', 'Entry']
    data.loc[~data['level'].isin(title_levels), 'level'] = 'not specified'

    return data
