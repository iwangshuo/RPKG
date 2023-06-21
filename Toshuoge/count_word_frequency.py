import csv

# package name
# package description
# index.csv

def get_text():
    csv_file = open('../data/index.csv', 'r')
    reader = csv.DictReader(csv_file)
    words = []
    for row in reader:
        pkg_name = row['package_name']
        name_words = pkg_name.split('_')
        words.extend(name_words)

        pkg_desc = row['package_description']
        desc_words = get_word_from_desc(pkg_desc)
        words.extend(desc_words)


        # print(words)
        # break
    return words
    pass

def get_word_from_desc(text):
    result = []
    words = text.split()
    for word in words:
        word = word.strip(',.()')
        word = word.lower()
        result.append(word)
    return result


# get_text() # Last_commit_date,package_description,package_name

counts = {}
words = get_text()
for word in words:
    counts[word] = counts.get(word,0) + 1
    pass


items = list(counts.items())
items.sort(key= lambda x:x[1],reverse=True)
count_csv = open('./word_frequency.csv', 'w', encoding='utf-8')
writer = csv.DictWriter(count_csv, ['word','count'])
writer.writeheader()
for item in items:
    word, count = item
    data = {'word':word, 'count':count}
    writer.writerow(data)
    pass
    # print("{0:<10}{1:>5}".format(word,count))


count_csv.close()