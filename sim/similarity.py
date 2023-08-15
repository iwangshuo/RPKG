from bert_serving.client import BertClient
import numpy as np

def cos_similar(sen_a_vec, sen_b_vec):
    vector_a = np.mat(sen_a_vec)
    vector_b = np.mat(sen_b_vec)
    num = float(vector_a*vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num/denom
    return cos

def similarity_bert(word1, word2):
    bc = BertClient(ip='localhost', check_version=False, check_length=False)
    vec1 = bc.encode([word1])
    vec2 = bc.encode([word2])
    sim = cos_similar(vec1, vec2)
    bc.close()
    return sim
# a = np.array([1,2,3])
# b = np.array([2,3,5])
# print(a)
# print("similarity", similarity_bert('get accessing', 'allow access'))   # 做排序比较有效
# print(similarity_bert("bringup", "bring up"))
# print(similarity_bert("grasp", "manipulation"))
# print(similarity_bert("ros", "robot"))
# print(similarity_bert("move", "grasp"))
# print(similarity_bert("start", "begin"))
# print(similarity_bert("bring up a robot", "wake up a robot"))


# rplidar   belong to cate


#      ----------------rplidar-------------------
# # cate:   score=0.7608016027063493
# print(similarity_bert("rplidar", "The rplidar ros package support rplidar A2/A1"))
# print(similarity_bert("rplidar", "A3/S1"))





#      ----------------rospeex-------------------
# # func    score=0.6390052141387589
# print(similarity_bert("rplidar", "defines messages"))
#
# # cate
# print(similarity_bert("rplidar", "This package"))  # score=0.6556417521050719,
# print(similarity_bert("rplidar", "rospeex."))  # score=0.8605491248445928,


# print('------------')
# print(similarity_bert("turtlebot","turtlebot2"))
# print(similarity_bert("turtlebot2","turtlebot"))
# print('------------')
# print(similarity_bert("turtlebot","turtlebot3"))
# print(similarity_bert("turtlebot2","turtlebot3"))



# print(similarity_bert("robot","robotics"))



# print("similarity", cos_similar(a, b))   # 做排序比较有效
# print("similarity1", cos_similar(a, b))   # 做排序比较有效
# print("similarity2", cos_similar(a, b))   # 做排序比较有效
# print("similarity3", cos_similar(a, b))   # 做排序比较有效
# print("similarity4", cos_similar(a, b))   # 做排序比较有效
# print("similarity5", cos_similar(a, b))   # 做排序比较有效
# print("similarity6", cos_similar(a, b))   # 做排序比较有效
# print("similarity7", cos_similar(a, b))   # 做排序比较有效
# print("similarity8", cos_similar(a, b))   # 做排序比较有效
# print("similarity9", cos_similar(a, b))   # 做排序比较有效

