
import os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv() 

KEY_PATH = os.environ.get('GCC_KEY_PATH')
property_id = os.environ.get('PROPERTY_ID')


class GAService():

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        self.client = BetaAnalyticsDataClient(credentials=credentials)

    def get_conversion_funnel_data(self, start_date, end_date):
        dimensions= ['eventName', 'date']
        metrics= ['activeUsers', 'totalUsers', 'eventCount']
        date_range= [
            {
                'start_date': start_date,
                'end_date': end_date
            }
        ]
        event_names_to_filter = ['session_start', 'view_cart', 'add_to_cart', 'begin_checkout', 'purchase']
        filter_expression = FilterExpression(
            filter=Filter(
                field_name='eventName',
                in_list_filter=Filter.InListFilter(values=event_names_to_filter)
            )
        )

        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name=dim) for dim in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
            date_ranges=[DateRange(**dr) for dr in date_range],
            dimension_filter=filter_expression
        )

        response = self.client.run_report(request)
        return response.rows
    
    def get_visitors_by_channel_data(self, start_date, end_date):
        dimensions= ['sessionMedium', 'date']
        # , 'date'
        # 'sessionCampaignId', 'transactionId', 'device_category', 'month', 'audience_name', 'hour'
        metrics= ['newUsers', 'totalUsers', 'eventCount']
        # 'total_revenue', 'transactions', 'sessions', 'views',
        date_range= [
            {
                'start_date': start_date,
                'end_date': end_date
            }
        ]
        source_to_filter = ['cpc', 'paidsocial', 'SMS', 'Email', 'Organic', 'Referral']
        filter_expression = FilterExpression(
            filter=Filter(
                field_name='sessionMedium',
                in_list_filter=Filter.InListFilter(values=source_to_filter)
            )
        )
        # filter_expression = FilterExpression(
        #     filter=Filter(
        #         field_name='sessionSourceMedium',
        #         string_filter=Filter.StringFilter(
        #             value='cpc',
        #             match_type=Filter.StringFilter.MatchType.CONTAINS
        #         )
        #     )
        # )
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name=dim) for dim in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
            date_ranges=[DateRange(**dr) for dr in date_range],
            dimension_filter=filter_expression
        )

        response = self.client.run_report(request)
        return response.rows

# Timezone check
today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_date = yesterday.strftime('%Y-%m-%d')

start_date = yesterday_date #'2024-08-14'
end_date = yesterday_date #'2024-08-14'
print(start_date ,end_date)


ga_service = GAService()
cf = ga_service.get_conversion_funnel_data(start_date, end_date)

# ------ CONVERSION FUNNEL -------------
print("------ CONVERSION FUNNEL -------------")
conversion_funnel_data = []
total_purchase = 0
total_session = 0
conversion_rate = 0
for row in cf:
    row_data = {
        "Event": row.dimension_values[0].value,
        "Date": {row.dimension_values[1].value},
        "Active Users": int(row.metric_values[0].value),
        "Total Users": int(row.metric_values[1].value),
        "Event Count": int(row.metric_values[2].value)
    }
    if row.dimension_values[0].value == "session_start":
        total_session = int(row.metric_values[2].value)
    if row.dimension_values[0].value == "purchase":
        total_purchase = int(row.metric_values[2].value)
    conversion_funnel_data.append(row_data)

if(total_session > 0):
    conversion_rate = total_purchase / total_session * 100

print(conversion_funnel_data)
print(total_purchase, total_session, conversion_rate)
print("--------------------------------------")


# ------ VISTIORS BY CHANNEL -------------
print("------ VISTIORS BY CHANNEL -------------") 
vbc = ga_service.get_visitors_by_channel_data(start_date, end_date)
vbc_data = []
for row in vbc:
    row_data = {
        "Event": row.dimension_values[0].value,
        "Date": {row.dimension_values[1].value},
        "New Users": int(row.metric_values[0].value),
        "Total Users": int(row.metric_values[1].value),
        "Event Count": int(row.metric_values[2].value)
    }
    vbc_data.append(row_data)

print(vbc_data)
print("--------------------------------------")