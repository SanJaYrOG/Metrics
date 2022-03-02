import boto3
import requests, json
import config
import datetime
from requests.auth import HTTPBasicAuth
from datetime import datetime

client = boto3.client('cloudwatch', region_name='ap-southeast-1')

config.PROD_URL
config.PROD_USER
config.PROD_PASS
config.AUTHENTICATION
config.HEADER
config.current_date



def lambda_handler(event,context):
    rr = get_docs_size_api(config.PROD_URL,config.HEADER,config.AUTHENTICATION)       
    cindex = create_app_indices_dict(config.current_date,rr)
    put_metrics_cloudwatch(cindex)

def get_docs_size_api(PROD_URL, Header, AUTHENTICATION):
    r = requests.get(PROD_URL + '_cat/indices?v&h=index,docs.count,store.size&bytes=mb&format=json&s=store.size:desc', auth=AUTHENTICATION, headers=config.HEADER)
    print('Response: {}'.format(r))
    return r

def create_app_indices_dict(current_date,r):
    current_indices = {}
    for index_dict in r.json():
        if current_date in index_dict['index']:            
            if "app" in index_dict['index']:                
                iname = index_dict['index'][14:-11]               
                current_indices[iname] = [index_dict['store.size'], index_dict['docs.count']]  
    return current_indices


def put_metrics_cloudwatch(current_indices):          
    for metric in current_indices:
        METRICDATAOBJ = [{
                'MetricName': 'docs.count',
                'Dimensions': [
                    {
                        'Name': 'DocsCount',
                        'Value': metric
                    },
                ],
                'Value': int(current_indices[metric][1]),
                'Unit': 'Count'
            },
            {
                'MetricName': 'store.size',
                'Dimensions': [
                    {
                        'Name': 'IndexSize',
                        'Value': metric
                    },
                ],
                'Value': float(current_indices[metric][0]),     
                'Unit': 'Megabytes'
            }]
        response = client.put_metric_data(
            Namespace='sanjay/test-local/example-from-internet',
            MetricData = METRICDATAOBJ
        )
        print(response) 
            
