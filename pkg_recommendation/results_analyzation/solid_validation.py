#! /usr/bin/env python
import pandas as pd
import csv
import argparse
import platform
import sys
import random

random.seed(7)



def compute_acc_from_rank(input_dir, output_dir):
    df = pd.read_csv(input_dir, encoding='utf-8')
    header = list(df.keys())  # 打印Name列

    print(header)
    # top 1 5 10 15 20


    with open(output_dir, 'w') as file:
        writer = csv.DictWriter(file, ['Sample Size', 'top1', 'top5', 'top10', 'top15', 'top20'])
        writer.writeheader()

        data = list(df["RPKG"])
        sample_range = [i for i in range(10,101,10)]
        # print(sample_range)
        for sample_size in sample_range:
            samples = random.sample(data, sample_size)


            top1, top5, top10, top15, top20 = 0,0,0,0,0
            for d in samples:
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

            datarow = {'Sample Size':sample_size, 'top1':top1/sample_size, 'top5':top5/sample_size, 'top10':top10/sample_size, 'top15':top15/sample_size, 'top20':top20/sample_size}
            writer.writerow(datarow)

if __name__ == '__main__':
    print('Python版本号：', platform.python_version())
    print('Python版本元组：', sys.version_info)
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank_input_dir', type=str, help='path to rank file')
    parser.add_argument('--acc_output_dir', type=str, help='path to output file')
    args = parser.parse_args()

    compute_acc_from_rank(args.rank_input_dir, args.acc_output_dir)


# ./solid_validation.py --rank_input_dir ./all_results.csv --acc_output_dir ./solid_result.csv