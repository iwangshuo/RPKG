import os
import csv
from py2neo import Graph, Node, Relationship
from bert_serving.client import BertClient

class Neo4jDataImporter:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", user="neo4j", password="/")
        self.category_node_dict = {}
        self.tag_node_dict = {}
        self.feature_word_dict = {}
        self.bc = BertClient(ip='localhost', check_version=False, check_length=False)

    def clear_graph(self):
        self.g.run("match (n) detach delete n")

    def import_package(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            for line in data_reader:
                node = Node("Package", package_name=line[2], package_description=line[1], last_commit_date=line[0])
                self.g.create(node)

    def import_repo(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            for line in data_reader:
                node = Node('Repository', name=line[2], repo_packages=line[1], repo_url=line[3], last_commit_date=line[0])
                self.g.create(node)
                if line[1] != "":

                    package_list = line[1].split(',')
                    for package in package_list:
                        pkg_node_matched = self.g.nodes.match("Package", package_name=package).first()
                        if pkg_node_matched is None:
                            continue
                        be_from_repo = Relationship(pkg_node_matched, 'is_from_repo', node)
                        self.g.create(be_from_repo)
                        pass

    def import_robot(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            for line in data_reader:
                line = [l.lower() for l in line]
                Robot = Node('Robot', name=line[1], category=line[2], website=line[3], wiki=line[4], description=line[5], tags=line[6])
                self.g.create(Robot)
                if line[2] != "":

                    if line[2] not in self.category_node_dict.keys():
                        Category = Node('Category', name=line[2])
                        self.g.create(Category)
                        self.category_node_dict[line[2]] = Category
                    belong_to_category = Relationship(Robot, "is_in_category", self.category_node_dict[line[2]])
                    self.g.create(belong_to_category)

                if line[6] != "":
                    tag_list = line[6].split(',')
                    for tagg in tag_list:

                        if tagg not in self.tag_node_dict.keys():
                            Tag = Node('Tag', name=tagg)
                            self.tag_node_dict[tagg] = Tag
                            self.g.create(Tag)

                        have_tag = Relationship(Robot, 'has_tag', self.tag_node_dict[tagg])
                        self.g.create(have_tag)
                        pass

    def import_sensor(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            for line in data_reader:
                line = [l.lower() for l in line]
                Sensor = Node('Sensor', name=line[2], url=line[1], sensor_type=line[3], package=line[4])
                self.g.create(Sensor)
                if line[3] != "":
                    if line[3] not in self.category_node_dict.keys():
                        SensorType = Node('Category', name=line[3])
                        self.g.create(SensorType)
                        self.category_node_dict[line[3]] = SensorType
                    belong_to_type = Relationship(Sensor, "is_in_category", self.category_node_dict[line[3]])
                    self.g.create(belong_to_type)

                if line[4] != "":
                    Package = self.g.nodes.match("Package", package_name=line[4]).first()
                    if Package:
                        apply_to = Relationship(Package, 'is_for_sensor', Sensor)
                        self.g.create(apply_to)

    def import_pkg_category(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            for line in data_reader:
                Package = self.g.nodes.match("Package", package_name=line[0]).first()

                if Package is None:
                    Package = Node('Package', package_name=line[0], package_description="", last_commit_date="")
                    self.g.create(Package)
                    print(line[0])
                if line[1] != "":
                    if line[1] not in self.category_node_dict.keys():
                        PackageType = Node('Category', name=line[1])
                        self.g.create(PackageType)
                        self.category_node_dict[line[1]] = PackageType

                    instance_of = Relationship(Package, "is_in_category", self.category_node_dict[line[1]])
                    self.g.create(instance_of)

    def import_pkg_file(self, filename, file_type, relation_name):
        path = os.path.join('../output', filename)

        with open(path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            i = 0
            for line in data_reader:
                Package = self.g.nodes.match('Package', package_name=line[0]).first()

                if line[1] != "":
                    FileType = Node(file_type, name=line[1])
                    self.g.create(FileType)

                    relation = Relationship(Package, relation_name, FileType)
                    self.g.create(relation)

                    if file_type == "Launch":
                        features = line[1].lower().split(".")[0].split("_")
                        for f_word in features:
                            if f_word == "":  # _filter_laser.launch
                                continue
                            if f_word not in self.feature_word_dict.keys():
                                # encode with bert and transform to string
                                vec1 = self.bc.encode([f_word])
                                string = ' '.join(map(str, vec1.ravel().tolist()))

                                Feature = Node("Characteristics", name=f_word, embeddings=string)
                                self.g.create(Feature)
                                self.feature_word_dict[f_word] = Feature

                            have_feature = Relationship(Package, "has_characteristics", self.feature_word_dict[f_word])
                            self.g.create(have_feature)

                print(i)
                i += 1

    def import_pkg_name_hardware_feature(self, filename):
        path = os.path.join('../output', filename)

        with open(path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            i = 0
            for line in data_reader:
                Package = self.g.nodes.match("Package", package_name=line[0]).first()

                if Package is None:
                    Package = Node('Package', package_name=line[0], package_description="", last_commit_date="")
                    self.g.create(Package)
                    print(line[0])
                if line[2] != "":
                    Robot = self.g.nodes.match("Robot", name=line[2]).first()
                    apply_to = None
                    if Robot:
                        apply_to = Relationship(Package, "is_for_robot", Robot)
                    else:
                        Sensor = self.g.nodes.match("Sensor", name=line[2]).first()

                        if Sensor:
                            apply_to = Relationship(Package, "is_for_sensor", Sensor)
                        else:
                            print(i, line[2])

                    self.g.create(apply_to)

                print(i)
                i += 1

    def import_pkg_characteristics(self, filename):
        path = os.path.join('../output', filename)

        with open(path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            i = 0
            for line in data_reader:
                line = [l.lower() for l in line]
                Package = self.g.nodes.match("Package", package_name=line[0]).first()

                if Package is None:
                    Package = Node('Package', package_name=line[0], package_description="", last_commit_date="")
                    self.g.create(Package)
                    print(line[0])
                if line[1] != "":
                    if line[1] not in self.feature_word_dict.keys():
                        # encode with bert and transform to string
                        vec1 = self.bc.encode([line[1]])
                        string = ' '.join(map(str, vec1.ravel().tolist()))

                        Feature = Node("Characteristics", name=line[1], embeddings=string)

                        self.g.create(Feature)
                        self.feature_word_dict[line[1]] = Feature

                    have_feature = Relationship(Package, "has_characteristics", self.feature_word_dict[line[1]])
                    self.g.create(have_feature)

                print(i)
                i += 1

    def import_pkg_function(self, filename):
        path = os.path.join('../output', filename)

        with open(path, 'r', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            header = next(data_reader)
            i = 0
            for line in data_reader:
                line = [l.lower() for l in line]
                Package = self.g.nodes.match("Package", package_name=line[0]).first()

                if Package is None:
                    Package = Node('Package', package_name=line[0], package_description="", last_commit_date="")
                    self.g.create(Package)
                    print(line[0])
                if line[1] != "":
                    if line[1] not in self.feature_word_dict.keys():
                        # encode with bert and transform to string
                        vec1 = self.bc.encode([line[1]])
                        string = ' '.join(map(str, vec1.ravel().tolist()))

                        Feature = Node("Function", name=line[1], embeddings=string)

                        self.g.create(Feature)
                        self.feature_word_dict[line[1]] = Feature

                    have_feature = Relationship(Package, "has_function", self.feature_word_dict[line[1]])
                    self.g.create(have_feature)

                print(i)
                i += 1

if __name__ == "__main__":
    importer = Neo4jDataImporter()
    importer.clear_graph()

    importer.import_package('../data/pkg_description.csv')
    importer.import_repo('../data/repo.csv')
    importer.import_robot('../data/robots.csv')
    importer.import_sensor('../data/sensors.csv')

    importer.import_pkg_category('../data/output/package_category.csv')
    importer.import_pkg_file('../data/output/package_node.csv', 'Node', 'includes_node')
    importer.import_pkg_file('../data/output/package_msg.csv', 'Message', 'includes_message')
    importer.import_pkg_file('../data/output/package_launch.csv', 'Launch', 'includes_launch')
    importer.import_pkg_file('../data/output/package_action.csv', 'Action', 'includes_action')
    importer.import_pkg_file('../data/output/package_srv.csv', 'Service', 'includes_service')

    importer.import_pkg_name_hardware_feature('../data/output/pkg_name_hardware_feature.csv')
    importer.import_pkg_characteristics('../data/output/package_characteristics.csv')
    importer.import_pkg_function('../data/output/package_function.csv')