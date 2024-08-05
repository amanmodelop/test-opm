import pandas as pd
import json
from pathlib import Path
from collections import Counter
import datetime


import modelop_sdk.apis.model_manage_api as mm_api
import modelop_sdk.restclient.moc_client as moc_client



#modelop.init
def init(job_json):
    global JOB
    global DEPLOYABLE_MODEL
    job = json.loads(job_json["rawJson"])
    DEPLOYABLE_MODEL = job.get("referenceModel", None)
    JOB = job_json

def metrics(df:pd.DataFrame):
    client = moc_client.MOCClient()    

    #STORED_MODEL_ID = DEPLOYABLE_MODEL.get("storedModel").get("id", "ID ERROR")
    opm={}
    opm["opm"]=""
    assets=DEPLOYABLE_MODEL.get("storedModel").get("modelAssets")
    for asset in assets:
        if 'TAG1' in asset["metaData"]["tags"]:
            opm["opm"]=True

    yield opm   

def main():
    raw_json=Path('example_job.json').read_text()
    init_param={'rawJson':raw_json}
    init(init_param)
    data = {"data1":993,"data2":36,"data3":3959,"label_value":0,"score":1}
    df = pd.DataFrame.from_dict([data])
    print(json.dumps(next(metrics(df)), indent=2))


if __name__ == '__main__':
	main()   
