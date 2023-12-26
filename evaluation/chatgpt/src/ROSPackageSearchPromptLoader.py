import json
from utils import Pattern
import csv

class ROSPackageSearchPromptLoader:

    def __init__(self, path, logger, start_idx, end_idx, model="gpt-3.5-turbo-0613", max_samples=100):
        self.path = path
        self.logger = logger
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.model = model
        self.max_samples = max_samples

    def load_data(self):
        data = []
        with open(self.path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        _data = []
        idx = self.start_idx
        for d in data[self.start_idx:self.end_idx]:
            query = {}
            for dim in ["robot", "sensor", "function", "characteristics", "repo", "node", "message", "service", "action", "launch", "category"]:
                if d[dim] != "":
                    query[dim] = d[dim].lower().split(',')
                else:
                    query[dim] = []
            # word = d['word']
            # print(query)
            _data.append([idx, str(query)])
            idx += 1
            if len(_data) >= self.max_samples:
                self.logger.info(f"Reach the max samples ({self.max_samples})")
                break
        return _data

    def generate(self):
        role_message = {"role": "system", "content": "Now you are an expert in recommending ROS package."}
        data = self.load_data()
        for d in data:
            self.logger.debug(d)
            prompt = Pattern.QUERY_JSON_PROMPT.replace("<QUERY>", d[1])
            self.logger.info(f"Prompt for {d[1]}: {prompt}")
            user_message = {"role": "user", "content": prompt}
            yield d[0], [role_message, user_message]


def write_test():
    data = [
        {"ChangeBefore": "rename a parameter", "ChangeAfter": "", "mode": "name"},
        {"ChangeBefore": "return fs.getPath(entryName);", "ChangeAfter": "rootPath = fs.getPath(entryName);", "mode": "before_and_after"}
            ]
    with open("test1.json", "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    pass
