import csv
import re
from datetime import datetime
# 2023-07-18 19:47:12,542 - utils - DEBUG - [10, "{'robot': [], 'sensor': ['leap_motion'], 'function': [], 'characteristics': ['ros driver'], 'repo': [], 'node': [], 'message': [], 'service': [], 'action': [], 'launch': [], 'category': []}"] - /Users/wshuo/PycharmProjects/MyKnowledgeGraph/Toshuoge/ROSPackageSearchPromptLoader.py:48
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')

log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (.+)')

def time_diff(last_time, timestamp):
    last = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S,%f')
    current = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
    time_difference = current - last
    return time_difference

time_record_list = []

def parse_logfile(logfile):
    with open(logfile, 'r') as file:
        log_content = file.readlines()

        last_time = None
        last_level = None
        for line in log_content:
            match = log_pattern.match(line)
            if match:
                timestamp, name, level, message = match.groups()
                if level == "INFO":
                    if last_level =="INFO":
                        # count difference
                        diff = time_diff(last_time, timestamp)
                        time_record_list.append(diff.total_seconds())
                    else:
                        last_time = timestamp
                last_level = level
            else:
                print(f"Invalid log format: {line}")

def output_csvfile(csvfile):
    csvfile = open(csvfile, 'w', encoding='UTF8', newline='')
    header = ['query_id', 'time(s)']
    writer = csv.writer(csvfile)
    writer.writerow(header)
    record_length = len(time_record_list)

    for i in range(record_length):
        data_row = [i+1, time_record_list[i]]
        writer.writerow(data_row)

    csvfile.close()


if __name__=="__main__":
    for i in range(0,100,10):
        logfile = "./log/test_package_search_{0}_{1}.log".format(i,i+10)
        parse_logfile(logfile)
    csvfile = "./query_time_chatgpt.csv"
    output_csvfile(csvfile)