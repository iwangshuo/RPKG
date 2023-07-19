import csv

desired_pkgs = []
with open('../../pkg_recommendation/user_queries.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        desired_pkgs.append(row['desired_package'])

print(len(desired_pkgs))

with open('./ranking.txt', 'w') as file:

    for i in range(100):
        txt_path = './package_search_{0}_0.txt'.format(i)
        txt_file = open(txt_path, 'r')
        rank_pkg = ''
        for line in txt_file.readlines():
            if desired_pkgs[i] in line:
                rank_pkg = line.split('.')[0]
                break
        if rank_pkg != '':
            file.write(rank_pkg+'\n')
        else:
            file.write('NA\n')

file.close()


