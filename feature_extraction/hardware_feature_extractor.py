import csv
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FeatureExtractor:
    def __init__(self):

        root_dir = '/'.join(os.path.abspath(__file__).split('/')[:-2])
        self.robot_path = os.path.join(root_dir, 'data/robots.txt')
        self.sensor_path = os.path.join(root_dir, 'data/sensors.txt')
        self.robot_common_words_path = os.path.join(root_dir, 'data/robot_common_words.txt')
        self.pkg_path = os.path.join(root_dir, 'data/pkg_description.csv')
        self.pkg_name_feature_path = os.path.join(root_dir, 'data/output/pkg_name_hardware_feature.csv')
        self.pkg_name_other_feature_path = os.path.join(root_dir, 'data/output/pkg_name_other_feature.csv')

        self.robot_wds = [i.strip().lower() for i in open(self.robot_path)]
        self.sensor_wds = [i.strip().lower() for i in open(self.sensor_path)]
        self.robot_common_wds = [i.strip().lower() for i in open(self.robot_common_words_path)]
        self.region_words = list(set(self.robot_wds + self.sensor_wds))

        self.feature_entity_dict = {}

    def extract_pkg_name(self):
        with open(self.pkg_name_other_feature_path, "w", newline="") as f1, \
                open(self.pkg_path, "r", encoding="unicode_escape") as f2, \
                open(self.pkg_name_feature_path, "w", newline="") as f3:
            reader2 = csv.DictReader(f2)
            column2 = [row["package_name"] for row in reader2]

            nr_writer = csv.writer(f1)
            writer = csv.writer(f3)
            header = ['package_name', 'feature_word', 'region_word', 'score']
            writer.writerow(header)
            for pkg_name in column2:
                words = pkg_name.split('_')
                non_region_words = words.copy()
                robot_name = words[0]

                # check if exist in dict
                if robot_name in self.feature_entity_dict.keys():
                    single_row = [pkg_name, robot_name, self.feature_entity_dict[robot_name][0],
                                  self.feature_entity_dict[robot_name][1]]
                    non_region_words.remove(robot_name)
                    writer.writerow(single_row)
                else:
                    fuzzy_match_results = process.extract(robot_name, self.region_words, limit=2)
                    match_region = fuzzy_match_results[0]

                    if match_region[1] >= 89:
                        # consider matched (like reemc--Reem-C, fuzzy=91)
                        single_row = [pkg_name, robot_name, match_region[0], match_region[1]]
                        if robot_name == "turtlebot":
                            single_row = [pkg_name, robot_name, "turtlebot2", 100]
                            non_region_words.remove(robot_name)
                            writer.writerow(single_row)
                            self.feature_entity_dict[robot_name] = ["turtlebot2", 100]
                        elif match_region[0] == 'bo':
                            if fuzzy_match_results[1][1] >= 89:
                                single_row = [pkg_name, robot_name, fuzzy_match_results[1][0],
                                              fuzzy_match_results[1][1]]
                                non_region_words.remove(robot_name)
                                writer.writerow(single_row)
                                self.feature_entity_dict[robot_name] = fuzzy_match_results[1][0]
                        elif robot_name not in self.robot_common_wds:
                            non_region_words.remove(robot_name)
                            writer.writerow(single_row)
                            self.feature_entity_dict[robot_name] = match_region[0]
                        else:
                            pass

                for nr_word in non_region_words:
                    single_row = [pkg_name, nr_word]
                    nr_writer.writerow(single_row)

if __name__ == "__main__":
    handler = FeatureExtractor()
    handler.extract_pkg_name()
    pass
