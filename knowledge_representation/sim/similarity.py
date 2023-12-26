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

if __name__ == "__main__":
    print(similarity_bert("rplidar", "rospeex"))
    print(similarity_bert("rplidar", "start rplidar sensor"))
    print(similarity_bert("moveit framework", "moveit library"))
    print(similarity_bert("gazebo simulator", "gazebo simulation environment"))
    print(similarity_bert("OMPL", "Open Manipulator Planning Library"))