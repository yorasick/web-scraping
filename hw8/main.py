import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_vacancies(page: int):
    driver = webdriver.Chrome()
    driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}')

    wait = WebDriverWait(driver, 10)

    list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ais-Hits-list")))
    items = list.find_elements(By.CLASS_NAME, "ais-Hits-item")

    vacancies = []
    for item in items:
        title = item.find_element(By.CLASS_NAME, "text-2xl").text
        url = item.find_element(By.TAG_NAME, "a").get_attribute("href")

        vacancies.append({
            "title": title,
            "url": url
        })

    return vacancies

if __name__ == "__main__":
    max_page = 2
    
    results = []

    for page in range(1, max_page + 1):
        results.extend(parse_vacancies(page))

    with open("output.json", "w") as f:
        json.dump(results, f, indent=4)
