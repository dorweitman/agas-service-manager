# This is a sample Python script.
import pandas as pd
import os
import json


def export_json_to_excel(pathToJsonFile):
    with open(pathToJsonFile) as json_file:
        participants_data = (json.load(json_file))["scores"]
        df = pd.DataFrame(participants_data)
        df.to_excel('DATAFILE.xlsx')
        return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathToJsonPushUpEvent = 'PushUpEvent.txt'
    pathToJsonRunEvent = 'RunEvent.txt'

    export_json_to_excel('score.txt')
