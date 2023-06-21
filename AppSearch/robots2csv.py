from bs4 import BeautifulSoup

import csv

html = open('/Users/wshuo/Desktop/data4KG/books-ckzz/robots.ros.org.html', encoding='utf-8')
soup = BeautifulSoup(html, features='html.parser')

csv_file = open('/Users/wshuo/Desktop/data4KG/robots.ros.org/robots.csv', 'w', encoding='UTF8', newline='')

header = ['robotID', 'robotName', 'category', 'website', 'wiki', 'description', 'tags']
writer = csv.writer(csv_file)
writer.writerow(header)


# //*[@id="grid"]/article[1]
#
# /html/body/section/main/div/article[1]

# print(soup.html.body.section.main.div.article)
articles = soup.find_all('article', itemscope="itemscope")
# print(articles)
count = 0
for a in articles:
    # / html / body / section / main / div / article[1] / div / a[1] / h2 / text()
    count += 1
    name = a.div.a.h2.string.lstrip()
    print(name)
    # / html / body / section / main / div / article[1] / div / div[1] / div[2] / ul[1] / li / a / span
    category = a.find('div', {'class':'resources'})
    if category != None:
        category = category.find('a').span.string
    print(category)
    # / html / body / section / main / div / article[1] / div / div[1] / div[2] / ul[2] / li / a / text()
    a_tag = a.find('div', {'class':'resources'})

    website = ''
    wiki = ''

    if a_tag!= None:
        a_tag = a_tag.find_all('a')

        for tag in a_tag:
            if tag.string == 'Website':
                website = tag['href']
                print(website)
            elif tag.string == 'Wiki':
                wiki = tag['href']
                print(wiki)
            else:
                pass

    description = a.find('p', {'class': 'description'}).string
    print(description)
    tag_labels = a.find('div', {'class': 'tags'}).find_all('a')
    tags = []
    for label in tag_labels:
        tags.append(label.string)
    print(tags)
    tags_str = ','.join(tags)
    print(tags_str)

    data_row = [count, name, category, website, wiki, description, tags_str]
    writer.writerow(data_row)

csv_file.close()


