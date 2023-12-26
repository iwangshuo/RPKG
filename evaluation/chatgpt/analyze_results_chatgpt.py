#!/usr/bin/env python
import csv
import os


def analyze_results(user_query, result_dir, ranking_csv):
    with open(user_query, encoding='utf-8') as file1, open(ranking_csv, 'w', encoding='utf-8') as file2:
        reader = csv.DictReader(file1)
        fieldnames = reader.fieldnames + ['ranking']
        writer = csv.DictWriter(file2, fieldnames=fieldnames)
        writer.writeheader()

        id = 0
        for row in reader:
            desired_pkg = row['desired_package']
            result_path = os.path.join(result_dir, 'package_search_{0}_0.txt'.format(id))
            id += 1
            with open(result_path, encoding='utf-8') as txt_file:
                ranking = ''
                for line in txt_file.readlines():
                    if desired_pkg in line:
                        ranking = line.split('.')[0]
                        break
                if ranking == '':
                    ranking = 'NA'

            row['ranking'] = ranking
            writer.writerow(row)


if __name__ == "__main__":
    user_query = "./user_queries_chatgpt.csv"
    search_result_dir = "./search_result"
    output_ranking_csv = "./ranking_chatgpt.csv"
    analyze_results(user_query, search_result_dir, output_ranking_csv)


