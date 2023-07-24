import csv

with open('../user_queries.csv', encoding='utf-8') as file1:
    reader = csv.DictReader(file1)
    id = 1
    rankings = []
    for row in reader:
        desired_pkg = row['desired_package']
        result_path = './results/{0}.csv'.format(id)
        id += 1
        kinetic_pkgs = []

        with open(result_path, encoding='utf-8') as file2:
            reader2 = csv.DictReader(file2)
            for line in reader2:
                if line['distro'] == "kinetic":
                    kinetic_pkgs.append(line['name'])
        if desired_pkg not in kinetic_pkgs:
            rankings.append('NA')
        else:
            rankings.append(str(kinetic_pkgs.index(desired_pkg)))
    for r in rankings:
        print(r)
