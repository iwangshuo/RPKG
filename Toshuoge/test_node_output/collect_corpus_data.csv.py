import csv

with open('./test_corpus_data.csv', 'w') as file:
    writer = csv.DictWriter(file, ['text', 'phrase_id'])
    writer.writeheader()

    for i in range(25):
        txt_path = './phrase_{0}_0.txt'.format(i)
        txt_file = open(txt_path, 'r')
        for line in txt_file.readlines():
            if len(line)>=30:
                line = line[line.find(' ') + 1:]
                line = line.strip('\n')
                line = line.lower()
                data_row = {'text':line, 'phrase_id':i}
                writer.writerow(data_row)
file.close()


