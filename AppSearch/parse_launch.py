import csv
import re

launch_csv = open('/Users/wshuo/Desktop/data4KG/ckzz/analyze_features/launches.csv', encoding='utf-8')
launch_reader = csv.DictReader(launch_csv)

app_csv = open('/Users/wshuo/Desktop/data4KG/ckzz/analyze_features/new_application.csv', encoding='utf-8')
app_reader = csv.DictReader(app_csv)

app_data = [row for row in app_reader]
launch_data = [row for row in launch_reader]
print(len(app_data))

num = 0
rosrun_count = 0
while num < len(launch_data):
    app_id = int(launch_data[num].get('applicationID'))
    extended_keys = ["applicationName", "url", "taskID", "robotName"]
    for ek in extended_keys:
        launch_data[num][ek] = app_data[app_id-1][ek]
    launch_data[num]["appDescription"] = app_data[app_id-1]["description"]
    launch_data[num]['launchID'] = num+1
    launch_data[num]["launchfile"] = ''
    launch_data[num]["package"] = ''
    launch_data[num]["node"] = ''
    launch_data[num]["singleLaunch"] = ''

    # TODO: extract the complete line to include the parameters,
    #  like "roslaunch turtlebot_gazebo amcl_demo.launch map_file:=<full path to map yaml file>"
    roslaunch_match = re.findall('roslaunch (.*) (.*)\.launch' , launch_data[num]["launchCode"])
    launch_data_copy = launch_data.pop(num)

    has_launch_or_node = False
    for i in range(len(roslaunch_match)):
        new_data = launch_data_copy.copy()
        new_data['launchID'] = num+1
        new_data['package'] = roslaunch_match[i][0]
        new_data['launchfile'] = roslaunch_match[i][1]
        new_data['singleLaunch'] = 'roslaunch ' + new_data['package'] + ' ' + new_data['launchfile'] + '.launch'
        launch_data.insert(num, new_data)
        has_launch_or_node = True
        num += 1
    rosrun_match = re.findall('rosrun (.*)\n', launch_data_copy["launchCode"])
    for i in range(len(rosrun_match)):
        rosrun_count += 1
        package_node = rosrun_match[i].split(' ')
        new_data = launch_data_copy.copy()
        new_data['singleLaunch'] = 'rosrun ' + rosrun_match[i]
        new_data['launchID'] = num+1
        if len(package_node)>1:
            new_data['package'] = package_node[0]
            new_data['node'] = package_node[1]
            launch_data.insert(num, new_data)
            has_launch_or_node = True
            num += 1
        pass
    if not has_launch_or_node:
        launch_data.insert(num, launch_data_copy)
        num += 1
    pass
print(rosrun_count)

#TODO: 'python xxx.py' need to parse

launch_csv.close()
app_csv.close()


new_launch = open('/Users/wshuo/Desktop/data4KG/ckzz/analyze_features/new_launch_code.csv', 'w', encoding='utf-8')
new_header = launch_data[0].keys()
print(new_header)

writer = csv.DictWriter(new_launch, new_header)
writer.writeheader()
writer.writerows(launch_data)
new_launch.close()