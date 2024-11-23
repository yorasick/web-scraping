from bs4 import BeautifulSoup
import requests
import re

def get_html_content(url) -> str:
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': agent})
    if not response.ok:
        raise Exception(f"Failed to get content from {url}")
    return response.text


def find_news_urls(html, count=5) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    main = soup.find("main", {"id": "main-content"})
    # find first container
    container = main.find("div", class_=re.compile('.*-Container'))
    # find top level list
    list = container.find("ul", class_=re.compile('.*-Grid'))
    # find all articles in the list (omit Live)
    articles = list.find_all("div", attrs={'type': 'article'})

    urls = []
    while len(urls) < count and len(articles) > 0:
        article = articles.pop(0)
        a = article.find('a', class_=re.compile('.*-PromoLink'))
        if a != None:
            urls.append(a.get("href"))

    return urls


def parse_related_topics(url) -> list[str]:
    html = get_html_content(url)
    soup = BeautifulSoup(html, "lxml")

    main = soup.find("main", {"id": "main-content"})
    topic_list = main.find("div", attrs={"data-component": "topic-list"})
    cluster_items = topic_list.find("ul", class_=re.compile('.*-ClusterItems'))
    topics = cluster_items.find_all("a")

    return [topic.get_text() for topic in topics]


if __name__ == "__main__":
    url = 'https://www.bbc.com'
    html = get_html_content(url+'/sport')
    top5_news_urls = find_news_urls(html, count=5)
    data = [{
        'Links': url + news_url,
        'Topics': parse_related_topics(url + news_url)
    } for news_url in top5_news_urls]
    print(data)
   