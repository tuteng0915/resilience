"""
Complete the conversion of csv to json for subsequent data processing
"""


import json


def fromCognitiveData(filepath:str = './data/CognitiveData_Cold.csv'):
    """
    Get a simplified json of the user performance
    [{
        userId=,
        Inhibition=,  1 - 0.01 * avg(Inhibition_RI_False_Alarms)
        Shifting=,    avg(Shifting_Shifting_Incongruent_Accuracy)
        Inversion=,   avg(Inversion_CogInhib_Incongruent_Accuracy, Inversion_Conflict_Resolution_Accuracy)
        Memory=,      avg(Memory_a_WM_Return_Efficiency)
    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    # load from csv

    # simplify user performance

    # formJson


def fromPreSelfReport(filepath:str = './data/Cold_Pre_selfreport.csv'):
    """
    Get a simplified json containing only the columns we care about
    [{


    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    # load from csv

    # formJson


def fromPostSelfReport(filepath:str = './data/Cold_Post_selfreport.csv'):
    """
    Get a simplified json containing only the columns we care about
    [{


    },]
    :param filepath
    :return: str(json), dict(userId: dict(..))
    """
    # load from csv

    # formJson

