import os
import csv
from py2neo import Graph, Node, Relationship

graph = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")

sensor_file = csv.reader(open('data/Sensor1.csv', 'r', encoding='utf-8'))
msg_file = csv.reader(open('data/msg.csv', 'r', encoding='utf-8'))
package_file = csv.reader(open('data/sensor_package1.csv', 'r', encoding='utf-8'))
motor_file = csv.reader(open('data/Motor1.csv', 'r', encoding='utf-8'))
for line in sensor_file:
    # 跳过第一行
    if line[0] == 'sensor_id':
        continue

    Sensor = Node('sensor', Sensor_name=line[2], Url=line[1], Sensor_type=line[3])
    Package = Node('package', Package_name=line[4])
#     relationship
    has_ros_package = Relationship(Sensor, 'has_ros_package', Package)

for line in msg_file:
    # 跳过第一行
    if line[0] == 'msg_id':
        continue

    Message = Node('message', Message_name=line[1], Message_type=line[2], Message_ros_type=line[3], Message_url=line[4])
#
# for line in package_file:
#     # 跳过第一行
#     if line[0] == 'sensor_package_id':
#         continue
#     Package = Node('package', Package_name=line[1], Node=line[2], Published_topic=line[4], Subscribed_topic=line[6], Service=line[8], Parameter=line[9])

# for line in motor_file:
#     # 跳过第一行
#     if line[0] == 'motor_id':
#         continue
#     Motor = Node('motor', Motor_name=line[1], )

    graph.create(Sensor)
    graph.create(Package)
    graph.create(Message)
    graph.create(has_ros_package)