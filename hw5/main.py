import requests
import re
import json
import sqlite3

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base


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

    vacancies: list[dict] = [{ 'id': i+1, 'title': title.strip(), 'url': urls[i].strip() } for (i, title) in enumerate(titles)]
    
    return vacancies


def write_json(filename: str, vacancies: list[dict]) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, indent=4, ensure_ascii=False)
        

def write_sqlite(filename: str, vacancies: list[dict]) -> None:
   
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


def read_sqlite(filename: str) -> list[dict]:
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    vacancies = cursor.execute('SELECT * FROM vacancies').fetchall()
    conn.close()
    return vacancies


def write_sqlalchemy(filename: str, data: list[dict]) -> None:
    engine = create_engine(f'sqlite:///{filename}')
    Base = declarative_base()

    class Vacancy(Base):
        __tablename__ = 'vacancies'
        id = Column(Integer, primary_key=True)
        title = Column(String)
        url = Column(String)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for vacancy in data:
        session.merge(Vacancy(**vacancy), load=True)

    session.commit()
    session.close()


def read_sqlalchemy(filename: str) -> list[dict]:
    engine = create_engine(f'sqlite:///{filename}')
    Base = declarative_base()

    class Vacancy(Base):
        __tablename__ = 'vacancies'
        id = Column(Integer, primary_key=True)
        title = Column(String)
        url = Column(String)

    Session = sessionmaker(bind=engine)
    session = Session()

    vacancies = session.query(Vacancy).all()

    session.close()

    return [vacancy.__dict__ for vacancy in vacancies]

if __name__ == '__main__':
    html = get_html_content()
    vacancies = parse_vacancies(html)
    write_json('output.json', vacancies)
    # write_sqlite('output.db', vacancies)
    # print(read_sqlite('output.db'))
    write_sqlalchemy('output.db', vacancies)
    print(read_sqlalchemy('output.db'))
