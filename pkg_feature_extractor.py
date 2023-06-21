import csv
import os
import ahocorasick
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class FeatureExtractor:
    def __init__(self):

        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.robot_path = os.path.join(cur_dir, 'data/robots.txt')
        self.sensor_path = os.path.join(cur_dir, 'data/sensors.txt')
        self.robot_common_words_path = os.path.join(cur_dir, 'data/robot_common_words.txt')
        self.pkg_path = os.path.join(cur_dir, 'data/index.csv')
        self.pkg_name_feature_path = os.path.join(cur_dir, 'output/pkg_name_feature-20230311.csv')
        self.pkg_name_other_feature_path = os.path.join(cur_dir, 'output/pkg_name_other_feature-20230311.csv')
        # 领域名词（机器人名字、传感器名字等）
        self.robot_wds = [i.strip().lower() for i in open(self.robot_path)]
        self.sensor_wds = [i.strip().lower() for i in open(self.sensor_path)]
        self.robot_common_wds = [i.strip().lower() for i in open(self.robot_common_words_path)]
        # 所有领域词
        self.region_words = list(set(self.robot_wds + self.sensor_wds))
        # 构造领域actree，暂时没有用
        self.region_tree = self.build_actree(self.region_words)

    def extract_pkg_name(self):
        with open(self.pkg_path, "r", encoding="unicode_escape") as f2:
            reader2 = csv.DictReader(f2)
            column2 = [row["package_name"] for row in reader2]
        f1 = open(self.pkg_name_other_feature_path, "w", newline="")
        nr_writer = csv.writer(f1)

        with open(self.pkg_name_feature_path, "w", newline="") as f3:
            writer = csv.writer(f3)
            header = ['package_name', 'feature_word', 'region_word', 'score']
            writer.writerow(header)
            for pkg_name in column2:
                words = pkg_name.split('_')
                non_region_words = words.copy()
                robot_name = words[0]
                # 直接比较 or 模糊匹配
                fuzzy_match_results = process.extract(robot_name, self.region_words, limit=2)
                # print(word, fuzzy_match_results)
                match_region = fuzzy_match_results[0]

                if match_region[1] >= 89:
                    # consider matched (like reemc--Reem-C, fuzzy=91)
                    # TODO: rosbot-robot, fuzzy=91, 所以当匹配词为ROSbot时,切换到第二个词。
                    single_row = [pkg_name, robot_name, match_region[0], match_region[1]]
                    if match_region[0] == 'bo':
                        if fuzzy_match_results[1][1] >= 89:
                            single_row = [pkg_name, robot_name, fuzzy_match_results[1][0], fuzzy_match_results[1][1]]
                            non_region_words.remove(robot_name)
                            writer.writerow(single_row)
                    elif robot_name not in self.robot_common_wds:
                        non_region_words.remove(robot_name)
                        writer.writerow(single_row)
                    else:
                        pass

                # else:
                #     for word in words:
                #         is_region = False
                #         for region_word in self.region_words:
                #             partial_ratio = fuzz.partial_ratio(word, region_word)
                #             if partial_ratio>=89 and len(word)>3:
                #                 single_row = [pkg_name, word, region_word, partial_ratio, 1]
                #                 writer.writerow(single_row)
                #                 is_region = True
                #         if is_region:
                #             non_region_words.remove(word)

                for nr_word in non_region_words:
                    single_row = [pkg_name, nr_word]
                    nr_writer.writerow(single_row)
        f1.close()
        pass

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree


if __name__ == "__main__":
    handler = FeatureExtractor()
    handler.extract_pkg_name()
    pass
