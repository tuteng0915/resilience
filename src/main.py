import json
from utils.dataPreprocess import dataPreprocess
from utils.csv2json import fromCognitiveData, fromPreSelfReport, fromPostSelfReport, fromBaseline
from utils.mergeJson import mergeJson


if __name__ == '__main__':
    mergeJson()
