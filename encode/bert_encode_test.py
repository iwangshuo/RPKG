from bert_serving.client import BertClient
import numpy as np
import csv
from sim.similarity import *


bc = BertClient(ip='localhost', check_version=False, check_length=False)

word1 = "bringup"
word2 = "bring up"

vec1 = bc.encode([word1])

vec2 = bc.encode([word2])



sim_score = cos_similar(vec1, vec2)
print(sim_score)
bc.close()


print(similarity_bert("dog","cat"))
print(similarity_bert("start","begin"))

print(similarity_bert("rplidar","dog"))

print(similarity_bert("turtlebot","turtlebot2"))
print(similarity_bert("turtlebot","turtlebot3"))
print(similarity_bert("turtlebot2","turtlebot3"))

print(similarity_bert("rplidar","using rplidar"))

print(similarity_bert("rplidar","rplidar A1"))

print(similarity_bert("rplidar","using rplidar A1"))

print(similarity_bert("rplidar","rospeex."))

print(similarity_bert("rplidar","rospeex"))
