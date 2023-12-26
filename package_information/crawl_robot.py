#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import csv


def request_url(url):
    session = requests.Session()
    session.trust_env = False
    response = session.get(url=url, verify=False)
    return response.content


def request_local_html(html_path):
    html = open(html_path, encoding='utf-8')
    return html


def crawl_robot(csv_file_path):
    # url = "https://robots.ros.org/"
    # response_content = request_url(url)
    html = "../data/robots.ros.org.html"
    response_content = request_local_html(html)
    soup = BeautifulSoup(response_content, features='html.parser')
    articles = soup.find_all('article', itemscope="itemscope")
    csv_file = open(csv_file_path, 'w', encoding='UTF8', newline='')
    writer = csv.writer(csv_file)
    header = ['robotID', 'robotName', 'category', 'website', 'wiki', 'description', 'tags']
    writer.writerow(header)
    count = 0
    for a in articles:
        count += 1
        # html tree may change, need review
        # / html / body / section / main / div / article[1] / div / a[1] / h2 / text()
        name = a.div.a.h2.string.lstrip()
        # / html / body / section / main / div / article[1] / div / div[1] / div[2] / ul[1] / li / a / span
        category = a.find('div', {'class': 'resources'})
        if category is not None:
            category = category.find('a').span.string
        # / html / body / section / main / div / article[1] / div / div[1] / div[2] / ul[2] / li / a / text()
        a_tag = a.find('div', {'class': 'resources'})
        website = ''
        wiki = ''
        if a_tag is not None:
            a_tag = a_tag.find_all('a')
            for tag in a_tag:
                if tag.string == 'Website':
                    website = tag['href']
                elif tag.string == 'Wiki':
                    wiki = tag['href']
                else:
                    pass

        description = a.find('p', {'class': 'description'}).string
        tag_labels = a.find('div', {'class': 'tags'}).find_all('a')
        tags = []
        for label in tag_labels:
            tags.append(label.string)
        tags_str = ','.join(tags)

        data_row = [count, name, category, website, wiki, description, tags_str]
        writer.writerow(data_row)

    csv_file.close()


if __name__ == "__main__":
    # crawl_robot("./demo.csv")
    crawl_robot("../data/robots.csv")
