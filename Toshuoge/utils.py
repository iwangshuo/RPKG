import json
import logging
import os
import pandas as pd

class Pattern:
    GENERATION_SIMPLE = "Please help me complete the following code snippet: \n"
    GENERATION_METHOD = "Please help me complete the method `<METHOD>` in the following code snippet: \n"
    GENERATION_STATEMENT = "Please help me complete the statement `<STATEMENT>` in the following code snippet: \n"

    CHANGE_CLASSIFICATION_NAME = "What change type (in corrective, preventive, adaptive and perfective) does <CHANGE_NAME> belong to?"
    CHANGE_CLASSIFICATION_INSERT = "What change type (in corrective, preventive, adaptive and perfective) does the insertion of `<TARGET_ELEMENT>` `<CHANGE_AFTER>` belong to?"
    CHANGE_CLASSIFICATION_DELETE = "What change type (in corrective, preventive, adaptive and perfective) does the deletion of `<TARGET_ELEMENT>` `<CHANGE_BEFORE>` belong to?"
    CHANGE_CLASSIFICATION_UPDATE = "What change type (in corrective, preventive, adaptive and perfective) does the adaptation from `<CHANGE_BEFORE>` to `<CHANGE_AFTER>` belong to?"

    ROS_NODE_PROMPT = "Please provide me with the function of ros node `<NODE_NAME>` in one sentence."
    CORPUS_PHRASE_PROMPT = "Please give me 20 paragraphs to explain the semantics of the phrase `<PHRASE>`, and each paragraph at most 100 words."
    QUERY_JSON_PROMPT = "The query in json is `<QUERY>`, please return me with 20 most related ROS packages."
class Logger:
    level_mappings = {'info': logging.INFO,
                      'debug': logging.DEBUG,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}

    def __init__(self, log_file, level='info'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.level_mappings[level])
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        # self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

def write_to_json(file_name, data):
    with open(file_name, 'w') as w:
        json.dump(data, w)

if __name__ == "__main__":
    # read output.json
    with open("output.json", encoding='utf-8') as f:
        data = json.load(f)
    # find the index of id 5158
    # for i, d in enumerate(data):
    #     if d['id'] == 5158:
    #         print(i)
    print(len(data))
