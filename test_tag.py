import re
import os
import json
import pandas as pd
from pathlib import Path
import numpy as np
import modelop.utils as utils


#import modelop_sdk.restclient.moc_client as moc_client



# modelop.init
def init(init_param):
    global DEPLOYABLE_MODEL

    job = json.loads(init_param["rawJson"])
    
    # Get the deployable model we are targeting
    DEPLOYABLE_MODEL = job.get('referenceModel', {})
    print(DEPLOYABLE_MODEL.get("id"))
    if not DEPLOYABLE_MODEL:
        raise ValueError('You must provide a reference model for this job of the model to pull the test results from')
    
    logger = utils.configure_logger()


#modelop.metrics
def metrics(data: pd.DataFrame):
    print("Running the metrics function") 
    opm={}

    logger = utils.configure_logger()    
    opm["opm"]=0
    pattern="OPM_202._Q."
    assets=DEPLOYABLE_MODEL.get("storedModel").get("modelAssets")
    for asset in assets:
        tags_list=asset["metaData"]["tags"]
        if any(re.search(pattern, tag) for tag in tags_list):
            opm["opm"]=1
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