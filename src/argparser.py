"""
    Implement of arg-parser
"""
import argparse
import json


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--path', type=str, default='./data/')
        # self.parser.add_argument('--module', type=str, default='cnn')
        # self.parser.add_argument('--config', type=str, default='./config/default.json')
        self.parser.add_argument('--debug', action='store_true')
        self.parser.add_argument('--inference', action='store_true')
        self.parser.add_argument('--test', action='store_true', default=False)
        self.args = self.parser.parse_args()


def load_config(config_path):
    """
    :param config_path: path of config.json
    :return: config: dict
    """
    with open(config_path) as f:
        return json.loads(f.read())

