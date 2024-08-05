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

	raw_json = Path('example_job.json').read_text()
	init_param = {'rawJson': raw_json}

	init(init_param)
	df = pd.read_csv('german_credit_data.csv')
	# data = '''
	#  	{"id":993,"duration_months":36,"credit_amount":3959,"installment_rate":4,"present_residence_since":3,"age_years":30,"number_existing_credits":1,"checking_status":"A11","credit_history":"A32","purpose":"A42","savings_account":"A61","present_employment_since":"A71","debtors_guarantors":"A101","property":"A122","installment_plans":"A143","housing":"A152","job":"A174","number_people_liable":1,"telephone":"A192","foreign_worker":"A201","gender":"male","label_value":0,"score":1}
	#  '''
	# data_dict = json.loads(data)
	# df = pd.DataFrame.from_dict([data_dict])
	print(json.dumps(next(metrics(df)), indent=2))


if __name__ == '__main__':
	main()
