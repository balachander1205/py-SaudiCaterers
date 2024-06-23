import uuid
from datetime import datetime
import pandas as pd

def get_uuid():
	now_1 = datetime.now()
	cur_datetime = now_1.strftime("%Y-%m-%d %H:%M")
	uid = uuid.uuid1()
	return cur_datetime, uid


# To get the || average flight time = arrival time - departure time
def get_avg_flight_intime(sales_order_details):
	ts_arrival = pd.DataFrame(sales_order_details['Date'].astype(str) +' '+ sales_order_details['Arrival Time'].astype(str),columns = ["arrival"])
	ts_departure = pd.DataFrame(sales_order_details['Date'].astype(str) +' '+ sales_order_details['Departure time'].astype(str),columns = ["departure"])
	ts_departure['departure'] = pd.to_datetime(ts_departure['departure'])
	ts_arrival['arrival'] = pd.to_datetime(ts_arrival['arrival'])
	average_time = pd.DataFrame(ts_arrival['arrival'] - ts_departure['departure'],columns = ["average_time"])
	flight_ts = [sales_order_details['Route'],sales_order_details['Flight Number'],ts_arrival['arrival'], ts_departure['departure'],average_time['average_time']]
	final_df = pd.concat(flight_ts, axis=1)
	return final_df