#! /usr/bin/env python
import pandas as pd
import csv
import argparse

def compute_acc_from_rank(input_dir, output_dir):
    df = pd.read_csv(input_dir, encoding='utf-8')
    header = list(df.keys())
    # print(header)
    with open(output_dir, 'w') as file:
        writer = csv.DictWriter(file, ['method', 'top1', 'top5', 'top10', 'top15', 'top20'])
        writer.writeheader()

        for method in header[1:]:
            print(method)
            data = df[method]
            length = len(data)
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank_input_dir', type=str, help='path to rank file')
    parser.add_argument('--acc_output_dir', type=str, help='path to output file')
    args = parser.parse_args()

    compute_acc_from_rank(args.rank_input_dir, args.acc_output_dir)


# ./NDCG.py --rank_input_dir ./category_feature_necessity.csv --acc_output_dir ./category_acc.csv
