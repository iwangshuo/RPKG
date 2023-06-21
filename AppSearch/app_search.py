import csv

### STEP 1: get the task category

task_file = open('/Users/wshuo/Desktop/data4KG/ckzz/parsed_tasks.csv', encoding='utf-8')
task_reader = csv.DictReader(task_file)


task_list = [0 for i in range(500)]
print("task categories with ids")
num = 0
for i in task_reader:
    # print(num)
    task_name = i.get('taskName')
    task_id = i.get('redirectID')
    if task_id != '0':
        continue
    else:
        task_id = i.get('taskID')
    task_list[int(task_id)] = task_name
    print('(' + task_id + ')' + task_name)
    num += 1
    pass

task_file.close()

task_id = eval(input('choose the category of your robotic task:'))
print(task_id)
print('you task: ' + task_list[task_id])


### STEP 2: get the hardware devices list


print("device types with ids")

device_file = open('/Users/wshuo/Desktop/data4KG/ckzz/ckzz-devices.csv', encoding='utf-8')
device_reader = csv.DictReader(device_file)

device_list = [0 for i in range(100)]
num = 0
for i in device_reader:
    # print(num)
    device_id = i.get('deviceID')
    device_name = i.get('deviceName')

    device_list[int(device_id)] = device_name
    print('(' + device_id + ')' + device_name)
    num += 1
    pass

device_file.close()



device_count = eval(input('how many devices in your robot:'))
print(device_count)
robot_devices = []
for i in range(device_count):
    input_device = input('id of device ' + str(i+1) + ":")
    robot_devices.append(input_device)
    print(device_list[int(input_device)])

# print(robot_devices)


### STEP 3: query the RappKG
from py2neo import Graph


from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.searcher = AnswerSearcher()

    def chat_main(self, task, robot):
        answer = "Hello! I'm KG4RP. I hope I can help you! "

        final_answers = self.searcher.search_main(task, robot)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

handler = ChatBotGraph()

# task_id, robot_devices

answer = handler.chat_main(task_id, robot_devices)
print('answer:', answer)


