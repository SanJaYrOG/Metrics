from requests.auth import HTTPBasicAuth
from datetime import datetime
PROD_URL = 'https://search-commons-prod-es-f4y22hd6irbdq2xdjj4f3usfaq.ap-southeast-1.es.amazonaws.com/'
PROD_USER = 'sanjay.soni'
PROD_PASS = 'JoSQlypjsnTfhqO1islI4/pfK74='

AUTHENTICATION = HTTPBasicAuth(PROD_USER, PROD_PASS)

HEADER = {"Content-Type": "application/json"}

current_date = datetime.strftime(datetime.now(), "%Y.%m.%d")
