import ahocorasick
import os
import csv







fre_path = "/Users/wshuo/Desktop/小论文/bert/uncased_L-12_H-768_A-12/vocab.txt"

vocab_wds = [i.strip().lower() for i in open(fre_path)]


with open('./word_frequency.csv', 'r') as file1:
    reader = csv.DictReader(file1)
    with open('./region_word_frequency.csv', 'w') as file2:
        writer = csv.DictWriter(file2, ['word', 'count'])
        writer.writeheader()
        for row in reader:
            word = row['word']
            count = row['count']
            if word in vocab_wds:
                continue
            data_row = {'word': word, 'count':count}
            writer.writerow(data_row)


file2.close()
file1.close()





