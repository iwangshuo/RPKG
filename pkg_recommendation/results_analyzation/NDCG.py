import pandas as pd
import csv

df = pd.read_csv('./all_results.csv', encoding='utf-8')
header = list(df.keys())  # 打印Name列

print(header)
# top 1 5 10 15 20


with open('./output_topn.csv', 'w') as file:
    writer = csv.DictWriter(file, ['method', 'top1', 'top5', 'top10', 'top15', 'top20'])
    writer.writeheader()

    for method in header[1:]:
        print(method)
        data = df[method]
        # print(data)
        length = len(data)
        # print(length)
        top1, top5, top10, top15, top20 = 0,0,0,0,0
        for d in data:
            # print(d)
            if d<0:
                continue
            if d==1:
                top1 += 1
            if d<=5:
                top5 += 1
            if d<=10:
                top10 += 1
            if d<=15:
                top15 += 1
            if d<=20:
                top20 += 1

        datarow = {'method':method, 'top1':top1/length, 'top5':top5/length, 'top10':top10/length, 'top15':top15/length, 'top20':top20/length}
        writer.writerow(datarow)

