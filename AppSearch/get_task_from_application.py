import csv


raw_file = open('/Users/wshuo/Desktop/data4KG/ckzz/application_name.csv', encoding='utf-8')
reader = csv.DictReader(raw_file)


task_file = open('/Users/wshuo/Desktop/data4KG/ckzz/parsed_tasks.csv', 'w', encoding='utf-8')
header = ['taskID','taskName', 'robotName', 'url', 'redirectID']
writer = csv.DictWriter(task_file, header)
writer.writeheader()

row_num = 0
for i in reader:
    row_num += 1
    print(row_num)
    application_name = i.get('applicationName')
    print(application_name)
    split_list1 = application_name.split(" ")
    robot_name = split_list1[0]
    split_list2 = application_name.split(" - ")
    length = len(split_list2)
    task_name = split_list2[-1]
    url = i.get('url')
    data = {'taskID': row_num, 'taskName': task_name, 'robotName': robot_name, 'url': url, 'redirectID': 0}
    writer.writerow(data)




raw_file.close()
task_file.close()
