import csv
from application_spider.spiders.youdao import connect

raw_file = open('/Users/wshuo/Desktop/data4KG/ckzz/applications.csv', encoding='utf-8')
reader = csv.DictReader(raw_file)

application_file = open('/Users/wshuo/Desktop/data4KG/ckzz/application_name.csv', 'w', encoding='utf-8')
header = ['applicationID','applicationName', 'description', 'url']
writer = csv.DictWriter(application_file, header)
writer.writeheader()

launch_file = open('/Users/wshuo/Desktop/data4KG/ckzz/launches.csv', 'w', encoding='utf-8')
header2 = ['launchID','launchCode', 'description', 'applicationID']
writer2 = csv.DictWriter(launch_file, header2)
writer2.writeheader()


name_list = []
id = 0
launch_id = 1
row_num = 0
for i in reader:
    row_num += 1
    # print(row_num)
    name = i.get('application_name')
    if name not in name_list:
        id += 1
        name_list.append(name)
        name_en = connect(name)
        description = i.get('description')
        if description == '':
            description_en = ''
        else:
            description_en = connect(description)
        data = {'applicationID':id, 'applicationName':name_en, 'description':description_en, 'url': i.get('url')}
        writer.writerow(data)

    # print('------'+i.get('launch_function')+'------')
    launch_description = i.get('launch_function')

    # print(i)
    # print(launch_description)
    launch_description_en = ''
    if launch_description != '':
        launch_description_en = connect(launch_description)
    data2 = {'launchID':launch_id, 'launchCode': i.get('launch_code'), 'description':launch_description_en, 'applicationID':id}
    writer2.writerow(data2)
    launch_id += 1
    # if id == 6:
    #     break

raw_file.close()
application_file.close()
launch_file.close()
