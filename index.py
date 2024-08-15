
import os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

from dotenv import load_dotenv

load_dotenv() 

##google cloud console key path
KEY_PATH = os.environ.get('GCC_KEY_PATH')
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

#property id from google analytics
property_id = os.environ.get('PROPERTY_ID')


dimensions= ['country', 'eventName']
metrics= ['activeUsers', 'eventCount']
date_range= [
    {
        'start_date': '2024-08-01',
        'end_date': '2024-08-07'
    }
]

request = RunReportRequest(
    property=f'properties/{property_id}',
    dimensions=[Dimension(name=dim) for dim in dimensions],
    metrics=[Metric(name=metric) for metric in metrics],
    date_ranges=[DateRange(**dr) for dr in date_range]
)

response = client.run_report(request)

for row in response.rows:
    print(f"Country: {row.dimension_values[0].value}, "
          f"Event: {row.dimension_values[1].value}, "
          f"Active Users: {row.metric_values[0].value}, "
          f"Event Count: {row.metric_values[1].value}")
