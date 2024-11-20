import requests
import re
import json
import sqlite3


def get_html_content():
    url = 'https://www.lejobadequat.com/emplois'
    response = requests.get(url)
    if not response.ok:
        raise Exception(f"Failed to fetch HTML content: {response.status_code}")
    return response.text


def parse_vacancies(html_content):
    title_pattern = r'<h3 class="jobCard_title m-0">(.*?)</h3>'
    titles: list[str] = re.findall(title_pattern, html_content)

    url_pattern = r'<a href="(.*?)".*class="jobCard_link"'
    urls: list[str] = re.findall(url_pattern, html_content)

    print(urls)

    vacancies: list[dict] = [{ 'id': i+1, 'title': title.strip(), 'url': urls[i].strip() } for (i, title) in enumerate(titles)]
    
    return vacancies


def save_to_json(filename: str, vacancies: list[dict]) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, indent=4, ensure_ascii=False)
        

def save_to_sqlite(filename: str, vacancies: list[dict]) -> None:
   
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    
    # Insert vacancies
    cursor.executemany(
        'INSERT OR REPLACE INTO vacancies (id, title, url) VALUES (?, ?, ?)',
        [(v['id'], v['title'], v['url']) for v in vacancies]
    )
    
    conn.commit()
    conn.close()


def read_from_sqlite(filename: str) -> list[dict]:
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    vacancies = cursor.execute('SELECT * FROM vacancies').fetchall()
    conn.close()
    return vacancies


if __name__ == '__main__':
    html = get_html_content()
    vacancies = parse_vacancies(html)
    save_to_json('output.json', vacancies)
    save_to_sqlite('output.db', vacancies)
    print(read_from_sqlite('output.db'))
