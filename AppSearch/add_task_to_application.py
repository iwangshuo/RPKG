import csv


raw_file = open('/Users/wshuo/Desktop/data4KG/ckzz/application_name.csv', encoding='utf-8')
reader = csv.DictReader(raw_file)

task_file = open('/Users/wshuo/Desktop/data4KG/ckzz/parsed_tasks.csv', encoding='utf-8')
task_reader = csv.DictReader(task_file)


data = [row for row in reader]




num = 0
for i in task_reader:
    print(num)
    robot_name = i.get('robotName')
    task_id = i.get('redirectID')
    if task_id == '0':
        task_id = i.get('taskID')
    data[num]['robotName'] = robot_name
    data[num]['taskID'] = task_id
    num += 1
    pass

raw_file.close()
task_file.close()
new_header = data[0].keys()
new_file = open('/Users/wshuo/Desktop/data4KG/ckzz/new_application.csv', 'w', encoding='utf-8')
writer = csv.DictWriter(new_file, new_header)
writer.writeheader()
writer.writerows(data)