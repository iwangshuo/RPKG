import csv
with open('./google_query_links.csv', 'w') as file:
    writer = csv.DictWriter(file, ['query_id', 'link'])
    writer.writeheader()

    with open('../user_queries.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        id = 1
        for line in reader:
            query_description = line['description']
            query_google = query_description.replace(' ', '+')
            query_google = "https://www.google.com/search?q=site%3Aros.org+OR+site%3Agithub.com+" + query_google
            datarow = {"query_id":id, "link":query_google}
            writer.writerow(datarow)
            id += 1
