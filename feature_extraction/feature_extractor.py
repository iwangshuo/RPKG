import os
import csv
import xml.etree.ElementTree as ET
import re
from feature_extraction.chunk.chunk import SentenceAnalyzer

def is_meta_pkg(path):
    cmake_file = os.path.join(path, "CMakeLists.txt")
    with open(cmake_file) as myfile:
        content = myfile.read()
        if 'catkin_metapackage()' in content and ('#catkin_metapackage()' not in content) and (
                '# catkin_metapackage()' not in content):
            return True
    return False


def get_pkg_name(path):
    package_xml_file = os.path.join(path, "package.xml")
    tree = ET.parse(package_xml_file)
    root = tree.getroot()
    name = root.find('name').text
    return name.strip()


def get_pkg_category(path):
    cmake_file = os.path.join(path, "CMakeLists.txt")
    package_name = get_pkg_name(path)

    with open(cmake_file) as myfile:
        content = myfile.read()
        if 'catkin_metapackage()' in content and ('#catkin_metapackage()' not in content) and (
                '# catkin_metapackage()' not in content):
            return package_name, 'meta_package'

    suffix = package_name.split('_')[-1]
    has_msg_folder = False
    has_mesh_folder = False

    for root, dirs, files in os.walk(path, topdown=True):
        if 'msg' in dirs:
            has_msg_folder = True
        if ('meshes' in dirs) or ('urdf' in dirs) or ('models' in dirs):
            has_mesh_folder = True
        break

    if suffix == "msgs" and has_msg_folder:
        return package_name, 'message_package'

    if suffix == "description" and has_mesh_folder:
        return package_name, 'description_package'

    return package_name, 'function_package'


def traverse_pkgs(source_path, output_dir):
    with open(os.path.join(output_dir, "package_path.txt"), 'w', encoding='utf-8') as pkg_path_file, open(
            os.path.join(output_dir, "package_category.csv"), 'w', encoding='utf-8') as pkg_category_file:
        pkg_category_header = ['packageName', 'category']
        pkg_category_writer = csv.DictWriter(pkg_category_file, pkg_category_header)
        pkg_category_writer.writeheader()

        for root, dirs, files in os.walk(source_path, topdown=True):
            for name in dirs:
                repo_path = os.path.join(root, name)
                for repo_root, repo_dirs, repo_files in os.walk(repo_path, topdown=True):
                    is_package = False
                    if ("package.xml" in repo_files) and "CMakeLists.txt" in repo_files:
                        is_package = True

                    paths = []
                    if is_package:
                        paths.append(repo_path)

                    if not is_package:
                        for repo_dir in repo_dirs:
                            package_path = os.path.join(repo_path, repo_dir)
                            for pkg_root, pkg_dirs, pkg_files in os.walk(package_path, topdown=True):
                                if ("package.xml" in pkg_files) and "CMakeLists.txt" in pkg_files:
                                    paths.append(package_path)
                                for pkg_dir in pkg_dirs:
                                    new_package_path = os.path.join(package_path, pkg_dir)
                                    for new_pkg_root, new_pkg_dirs, new_pkg_files in os.walk(new_package_path,
                                                                                             topdown=True):
                                        if ("package.xml" in new_pkg_files) and "CMakeLists.txt" in new_pkg_files:
                                            paths.append(new_package_path)
                                        break
                                    break
                                break

                    for path_pkg in paths:
                        pkg_path_file.write(path_pkg + '\n')
                        package_name, package_type = get_pkg_category(path_pkg)
                        if package_type:
                            data_type = {'packageName': package_name, 'type': package_type}
                            pkg_category_writer.writerow(data_type)
                    break
            break
    print("traverse done!")


def parse_cmakelist(package_path):
    cmake_file_path = os.path.join(package_path, "CMakeLists.txt")
    cmake_file = open(cmake_file_path, "r")
    cmake_data = cmake_file.read()

    executable_regex = r"add_executable\((\S+) (\S+.cpp|\S+.c|\S+.cxx|\S+.cc|\S+.c\+\+|)"
    executable_matches = re.findall(executable_regex, cmake_data)

    node_files = []
    for match in executable_matches:
        executable_name = match[0]
        if executable_name != "${PROJECT_NAME}_node":
            if executable_name == "${PROJECT_NAME}":
                package_name = get_pkg_name(package_path)
                node_files.append(package_name)
            else:
                node_files.append(executable_name)

    script_folder = os.path.join(package_path, "scripts")
    if os.path.isdir(script_folder):
        node_files = [f for f in os.listdir(script_folder) if f.endswith(".py")]

    msg_folder = os.path.join(package_path, "msg")
    msg_files = []
    if os.path.isdir(msg_folder):
        msg_files = [f for f in os.listdir(msg_folder) if f.endswith(".msg")]

    srv_folder = os.path.join(package_path, "srv")
    srv_files = []
    if os.path.isdir(srv_folder):
        srv_files = [f for f in os.listdir(srv_folder) if f.endswith(".srv")]

    action_folder = os.path.join(package_path, "action")
    action_files = []
    if os.path.isdir(action_folder):
        action_files = [f for f in os.listdir(action_folder) if f.endswith(".action")]

    launch_folder = os.path.join(package_path, "launch")
    launch_files = []
    if os.path.isdir(launch_folder):
        launch_files = [f for _, _, files in os.walk(launch_folder, topdown=True) for f in files if
                        f.endswith((".launch.xml", ".launch"))]

    result = dict()
    result['node'] = node_files
    result['msg'] = msg_files
    result['srv'] = srv_files
    result['action'] = action_files
    result['launch'] = launch_files

    return result


def save_parse_result(package_path_file, output_dir):
    file = open(package_path_file, 'r', encoding='utf-8')

    pkg_launch_path = os.path.join(output_dir, "package_launch.csv")
    pkg_launch_csv = open(pkg_launch_path, 'w', encoding='utf-8')
    pkg_launch_header = ['packageName', 'launch']
    pkg_launch_writer = csv.DictWriter(pkg_launch_csv, pkg_launch_header)
    pkg_launch_writer.writeheader()

    pkg_node_path = os.path.join(output_dir, "package_node.csv")
    pkg_node_csv = open(pkg_node_path, 'w', encoding='utf-8')
    pkg_node_header = ['packageName', 'node']
    pkg_node_writer = csv.DictWriter(pkg_node_csv, pkg_node_header)
    pkg_node_writer.writeheader()

    pkg_srv_path = os.path.join(output_dir, "package_srv.csv")
    pkg_srv_csv = open(pkg_srv_path, 'w', encoding='utf-8')
    pkg_srv_header = ['packageName', 'srv']
    pkg_srv_writer = csv.DictWriter(pkg_srv_csv, pkg_srv_header)
    pkg_srv_writer.writeheader()

    pkg_action_path = os.path.join(output_dir, "package_action.csv")
    pkg_action_csv = open(pkg_action_path, 'w', encoding='utf-8')
    pkg_action_header = ['packageName', 'action']
    pkg_action_writer = csv.DictWriter(pkg_action_csv, pkg_action_header)
    pkg_action_writer.writeheader()

    pkg_msg_path = os.path.join(output_dir, "package_msg.csv")
    pkg_msg_csv = open(pkg_msg_path, 'w', encoding='utf-8')
    pkg_msg_header = ['packageName', 'msg']
    pkg_msg_writer = csv.DictWriter(pkg_msg_csv, pkg_msg_header)
    pkg_msg_writer.writeheader()

    for line in file:
        path = line.strip("\n")
        print(path)
        package_name = get_pkg_name(path)

        if is_meta_pkg(path):
            continue
        result = parse_cmakelist(path)
        for node in result['node']:
            data_row = {'packageName': package_name, 'node': node}
            pkg_node_writer.writerow(data_row)
        for msg in result['msg']:
            data_row = {'packageName': package_name, 'msg': msg}
            pkg_msg_writer.writerow(data_row)
        for action in result['action']:
            data_row = {'packageName': package_name, 'action': action}
            pkg_action_writer.writerow(data_row)
        for launch in result['launch']:
            data_row = {'packageName': package_name, 'launch': launch}
            pkg_launch_writer.writerow(data_row)
        for srv in result['srv']:
            data_row = {'packageName': package_name, 'srv': srv}
            pkg_srv_writer.writerow(data_row)

    file.close()
    pkg_launch_csv.close()
    pkg_srv_csv.close()
    pkg_action_csv.close()
    pkg_msg_csv.close()
    pkg_node_csv.close()
    print("result saved!")


def get_pkg_function_characteristics(pkg_description_file, output_dir):
    with open(pkg_description_file, "r") as file1, \
            open(os.path.join(output_dir, "package_characteristics.csv"), "w", newline="") as file2, \
            open(os.path.join(output_dir, "package_function.csv"), "w", newline="") as file3:
        reader = csv.DictReader(file1)
        ct_writer = csv.writer(file2)
        ct_writer.writerow(["package_name", "characteristics"])
        func_writer = csv.writer(file3)
        func_writer.writerow(["package_name", "function"])
        for row in reader:
            desc = row["package_description"]
            package = row["package_name"]
            if desc == "":
                continue
            analyzer = SentenceAnalyzer(desc)
            characteristics_list = analyzer.characteristics_list()
            function_list = analyzer.function_list()
            # print(characteristics_list)
            for ct in characteristics_list:
                data_row = [package, ct]
                ct_writer.writerow(data_row)
            for func in function_list:
                data_row = [package, func]
                func_writer.writerow(data_row)


if __name__ == "__main__":
    # Example usage:
    source_path = "/home/wshuo/Documents/data4KG/packages/source"
    output_dir = "../data/output"
    traverse_pkgs(source_path, output_dir)
    package_path_file = os.path.join(output_dir, "package_path.txt")
    save_parse_result(package_path_file, output_dir)
    pkg_description_file = "../data/pkg_description.csv"
    get_pkg_function_characteristics(pkg_description_file, output_dir)

