import os
import csv
from py2neo import Graph, Node, Relationship
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
from bert_serving.client import BertClient
from tqdm import tqdm
import time, math
from joblib import Parallel, delayed
import multiprocessing

class PackageAnalyzer:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", user="neo4j", password="/")
        self.package_all = {}
        self.data = self.fetch_package_data()
        self.query_template = {
                    'robot': [], "sensor": [], "function": [],
                    "characteristics": [], "repo": [], "node": [],
                    "message": [], "service": [], "action": [],
                    "launch": [], "robot_tag": [], "category": []
                }
        self.process_package_data(self.data)
        self.query_list = None
        self.scores = None
        self.scores_detail = None

    def fetch_package_data(self):
        data = self.g.run('MATCH (n:Package)-[r]-(d) RETURN n,r,d').data()
        return data

    def process_package_data(self, data):
        for item in data:
            package_name = item['n'].get('package_name')
            if package_name not in self.package_all.keys():
                self.package_all[package_name] = self.query_template
            d = item['d']
            label = str(d.labels)
            self.update_package_all(package_name, d, label)

    def update_package_all(self, package_name, d, label):
        if label == ":Category":
            self.package_all[package_name]["category"].append(d.get("name"))
        elif label == ":Robot":
            self.package_all[package_name]["robot"].append(d.get("name"))
        elif label == ":Sensor":
            self.package_all[package_name]["sensor"].append(d.get("name"))
        elif label == ":Characteristics":
            embeddings = np.fromstring(d.get("embeddings"), sep=' ').reshape((1, 768))
            self.package_all[package_name]["characteristics"].append(embeddings)
        elif label == ":Function":
            embeddings = np.fromstring(d.get("embeddings"), sep=' ').reshape((1, 768))
            self.package_all[package_name]["function"].append(embeddings)
        elif label == ":Repository":
            self.package_all[package_name]["repo"].append(d.get("name"))
        elif label == ":Node":
            self.package_all[package_name]["node"].append(d.get("name"))
        elif label == ":Messsage":
            self.package_all[package_name]["message"].append(d.get("name"))
        elif label == ":Service":
            self.package_all[package_name]["service"].append(d.get("name"))
        elif label == ":Action":
            self.package_all[package_name]["action"].append(d.get("name"))
        elif label == ":Launch":
            self.package_all[package_name]["launch"].append(d.get("name"))
        elif label == ":Tag":
            self.package_all[package_name]["robot_tag"].append(d.get("name"))
        else:
            pass

    def ld_distance(self, q_words, p_words):
        if len(q_words) == 0 or len(p_words) == 0:
            return 0
        scores = []
        for p in p_words:
            # assume just one phrase in q-word
            score = fuzz.partial_ratio(p, q_words[0])
            scores.append(score)
        return max(scores) / 100

    def sgn_similarity(self, q_words, p_words):
        if len(q_words) == 0 or len(p_words) == 0:
            return 0
        # remove extension for names
        q_names = [name.split('.')[0].lower() for name in q_words]
        p_names = [name.split('.')[0].lower() for name in p_words]
        sgn = 0
        for name in q_names:
            if name in p_names:
                sgn += 1
        return sgn / len(q_words)

    def cos_similar(self, sen_a_vec, sen_b_vec):
        vector_a = np.mat(sen_a_vec)
        vector_b = np.mat(sen_b_vec)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        return cos

    def cosine_similarity(self, q_words, p_words):
        if len(q_words) == 0 or len(p_words) == 0:
            return 0
        q_embeddings = q_words
        p_embeddings = p_words  # [np.fromstring(word, sep=' ').reshape((1,768)) for word in p_words]

        score = 0
        for q_e in q_embeddings:
            max_cos = 0
            for p_e in p_embeddings:
                cos = self.cos_similar(q_e, p_e)
                if cos > max_cos:
                    max_cos = cos
            score += max_cos
        return score / len(q_words)

    def sim_q_p(self, query, p_features):
        score = {"robot": 0, "sensor": 0, "function": 0,
                 "characteristics": 0, "repo": 0, "node": 0,
                 "message": 0, "service": 0, "action": 0,
                 "launch": 0, "category": 0}

        for dim in score.keys():
            if dim in ["robot", "sensor"]:
                score[dim] = self.ld_distance(query[dim], p_features[dim])
            elif dim in ["function", "characteristics"]:
                score[dim] = 0.8 * self.cosine_similarity(query[dim], p_features[dim])
            elif dim in ["repo", "node", "message", "service", "action", "launch", "category"]:
                score[dim] = self.sgn_similarity(query[dim], p_features[dim])
            else:
                print("unknown dimension:", dim)

        return score

    def pkg_scores(self, query, package_all):
        scores = {}
        scores_detail = {}
        for p_name, features in tqdm(package_all.items()):
            score = self.sim_q_p(query, features)
            sum_score = sum(score.values())

            scores[p_name] = sum_score / len(score)
            scores_detail[p_name] = score
        return scores, scores_detail

    def pkg_score_parallel_multi_query(self, p_name, features):
        q_len = len(self.query_list)
        for i in range(q_len):
            score = self.sim_q_p(self.query_list[i], features)
            sum_score = sum(score.values())

            self.scores[i][p_name] = sum_score / len(score)
            self.scores_detail[i][p_name] = score

    def preprocess_query_list(self, path):
        csv_file = open(path, 'r')
        reader = csv.DictReader(csv_file)
        bc = BertClient(ip='localhost', check_version=False, check_length=False)

        query_list = []
        for row in reader:
            raw_query = row.copy()
            for dim in raw_query.keys():
                if raw_query[dim] != "":
                    if dim in ['function', 'characteristics']:
                        function_wds = raw_query[dim].split(',')
                        function_embeddings = [bc.encode([word]) for word in function_wds]
                        raw_query[dim] = function_embeddings
                    elif dim in ["robot", "sensor", "repo", "node", "message", "service", "action", "launch", "category"]:
                        raw_query[dim] = raw_query[dim].lower().split(',')
                    else:
                        pass
                else:
                    raw_query[dim] = []

            query_list.append(raw_query)
        bc.close()
        return query_list

    def run_analysis(self, query_list_path):
        self.query_list = self.preprocess_query_list(query_list_path)
        print(len(self.query_list))

        self.scores = [{} for _ in range(len(self.query_list))]
        self.scores_detail = [{} for _ in range(len(self.query_list))]

        start = time.time()
        num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores, require='sharedmem')(
            delayed(self.pkg_score_parallel_multi_query)(p_name, features) for p_name, features in
            self.package_all.items())
        end = time.time()
        print('{:.4f} s'.format(end - start))

        sorted_scores = [[] for _ in range(len(self.query_list))]

        for i in range(len(self.query_list)):
            sorted_scores[i] = sorted(self.scores[i].items(), key=lambda x: x[1], reverse=True)
            k = 1
            found = False
            for package_name, score in sorted_scores[i]:
                if package_name == self.query_list[i]['desired_package']:
                    print(k)
                    found = True
                    break
                k += 1
                if k > 20:
                    break
            if not found:
                print("NA")

if __name__ == "__main__":
    analyzer = PackageAnalyzer()
    analyzer.run_analysis("../evaluation/rpkg/user_queries_rpkg.csv")
    # user_query_dir = "../evaluation/rpkg/ablation_experiments/user_queries/"
    # analyzer.run_analysis(os.path.join(user_query_dir, "user_queries_robot.csv"))
    # analyzer.run_analysis(os.path.join(user_query_dir, "user_queries_sensor.csv"))
    # analyzer.run_analysis(os.path.join(user_query_dir, "user_queries_category.csv"))
    # analyzer.run_analysis(os.path.join(user_query_dir, "user_queries_function.csv"))
    # analyzer.run_analysis(os.path.join(user_query_dir, "user_queries_characteristics.csv"))
