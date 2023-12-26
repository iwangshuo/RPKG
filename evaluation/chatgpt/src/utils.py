import json
import logging

class Pattern:
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
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

def write_to_json(file_name, data):
    with open(file_name, 'w') as w:
        json.dump(data, w)

if __name__ == "__main__":
    with open("output.json", encoding='utf-8') as f:
        data = json.load(f)
    print(len(data))
