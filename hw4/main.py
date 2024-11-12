import requests
import re

def get_html_content():
    url = 'https://www.lejobadequat.com/emplois'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch HTML content: {response.status_code}")
    return response.text

def get_vacancies(html_content):
    title_pattern = r'<h3 class="jobCard_title m-0">(.*?)</h3>'
    titles = re.findall(title_pattern, html_content)

    url_pattern = r'<a href="(.*?)".*class="jobCard_link"'
    urls = re.findall(url_pattern, html_content)

    titles = [{ "title": title.strip(), "url": url.strip() } for (title, url) in zip(titles, urls)]
    
    return titles

if __name__ == '__main__':
    html = get_html_content()
    vacancies = get_vacancies(html)
    print(vacancies)