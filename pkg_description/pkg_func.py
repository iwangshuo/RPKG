import csv
import chunk.chunk_func_cate_simplify
from chunk import chunk_func_cate_simplify

with open("../data/index.csv", "r") as file1:
    reader = csv.DictReader(file1)
    desc = []
    package = []
    for row in reader:
        desc.append(row["package_description"])
        package.append(row["package_name"])
    print(type(desc))
    print(len(desc))
    print(len(package))
    with open("../output/pkg_func_wshuo.csv", "w", newline="") as file2:

        writer = csv.writer(file2)

        writer.writerow(["package_name", "function"])

        j = 1
        for i in range(0, len(desc)-1):
            if desc[i] == "":
                j += 1
                continue
            func_list = chunk_func_cate_simplify.function_list(desc[i])
            print("第"+str(j)+"个func_list:")
            print(func_list)

            for func in func_list:
                pkg_func_row = [package[i], func]
                writer.writerow(pkg_func_row)



            # cate_list = chunk_func_cate_simplify.category_list(desc[i])
            # print("第"+str(j)+"个cate_list:")
            # print(cate_list)
            j = j + 1