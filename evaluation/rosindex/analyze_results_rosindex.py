#!/usr/bin/env python
import csv
import os

def analyze_results(user_query, result_dir, ranking_csv):
    with open(user_query, encoding='utf-8') as file1, open(ranking_csv, 'w', encoding='utf-8') as file2:
        reader = csv.DictReader(file1)
        fieldnames = reader.fieldnames + ['ranking']
        writer = csv.DictWriter(file2, fieldnames=fieldnames)
        writer.writeheader()

        id = 1
        for row in reader:
            desired_pkg = row['desired_package']
            result_path = os.path.join(result_dir, '{0}.csv'.format(id))
            id += 1
            kinetic_pkgs = []
            with open(result_path, encoding='utf-8') as file2:
                result_reader = csv.DictReader(file2)
                for line in result_reader:
                    if line['distro'] == "kinetic":
                        kinetic_pkgs.append(line['name'])
            if desired_pkg not in kinetic_pkgs:
                ranking = 'NA'
            else:
                ranking = str(kinetic_pkgs.index(desired_pkg))
            row['ranking'] = ranking
            writer.writerow(row)


if __name__ == "__main__":
    user_query = "./user_queries_rosindex.csv"
    search_result_dir = "./search_result"
    output_ranking_csv = "./ranking_rosindex.csv"
    analyze_results(user_query, search_result_dir, output_ranking_csv)
