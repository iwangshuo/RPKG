import json
import os
# import tiktoken
from utils import Pattern
import csv

class ROSNodePromptLoader:

    def __init__(self, path, logger, start_idx, end_idx, model="gpt-3.5-turbo-0301", max_samples=100):
        self.path = path
        self.logger = logger
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.model = model
        self.max_samples = max_samples

    def load_data(self):
        # with open(self.path, 'r') as f:
        #     data = json.load(f)
        # TODO: transfer processing method to load csv file
        data = []
        with open(self.path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        _data = []
        idx = self.start_idx
        for d in data[self.start_idx:self.end_idx]:
            word = d['word']
            # count = d['count']
            # useless = d['useless']
            _data.append([idx, word])
            idx += 1
            if len(_data) >= self.max_samples:
                self.logger.info(f"Reach the max samples ({self.max_samples})")
                break
        return _data

    def generate(self):
        role_message = {"role": "system", "content": "You are an expert in ROS and robotics."}
        data = self.load_data()
        for d in data:
            self.logger.debug(d)
            prompt = Pattern.CORPUS_PHRASE_PROMPT.replace("<PHRASE>", d[1])
            self.logger.info(f"Prompt for {d[1]}: {prompt}")
            user_message = {"role": "user", "content": prompt}
            yield d[0], [role_message, user_message]

    # def count_tokens(self, prompt):
    #     try:
    #         encoding = tiktoken.encoding_for_model(self.model)
    #     except KeyError:
    #         self.logger.error(f"{self.model} not found")
    #         encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    #     return len(encoding.encode(prompt))

def write_test():
    # data = [
    #     {"code": "def train():\n\tpass", "target": "train", "granularity": "method"},
    #     {"code": "def test():\n\tpass", "target": "test", "granularity": "class"},
    # ]
    data = [
        {"ChangeBefore": "rename a parameter", "ChangeAfter": "", "mode": "name"},
        {"ChangeBefore": "return fs.getPath(entryName);", "ChangeAfter": "rootPath = fs.getPath(entryName);", "mode": "before_and_after"}
            ]
    with open("test1.json", "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    # write_test()
    # dataset_path = "C:\\Users\\24426\\Desktop\\ChatGPT-API"
    # prompt_loader = ChangeClassificationPromptLoader(os.path.join(dataset_path, 'test1.json'), 0, 2)
    # # data = prompt_loader.load_code()
    # for idx, d in prompt_loader.generate():
    #     print(idx, d)
    pass
