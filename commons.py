import uuid
from datetime import datetime
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory,json,Response


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
	average_time = pd.DataFrame(ts_arrival['arrival'] - ts_departure['departure'],columns = ["time_difference"])
	total_flights = sales_order_details.groupby(['Flight Number']).size().reset_index(name='total_flights')
	print("total_flights=",len(total_flights))
	average_flight_in_time = average_time["time_difference"].mean()
	avg_flight_time = str(average_flight_in_time).split(".")[0]
	print("avg_flight_time=",avg_flight_time)
	flight_ts = [sales_order_details['Route'],sales_order_details['Flight Number'],ts_arrival['arrival'].astype(str), ts_departure['departure'].astype(str),average_time['time_difference'].astype(str)]
	final_df = pd.concat(flight_ts, axis=1)
	return final_df, avg_flight_time

def get_meals_monthly_formatted_data(dataframe):
	month_labels = get_month_label()
	new_data = []
	try:
		not_found = True
		for item in dataframe:
			for month in new_data:
				not_found = True
				if item['month'] == month['month']:
					not_found = False
					month[item["Item category"]] = item['orders']
					break
			if not_found:
				data = {'month':item['month'], item["Item category"]:item['orders'],'Item':item['Item']}
				new_data.append(data)
		# update month to text label
		field_key = 'month'
		for new_item in new_data:
			if field_key in new_item:
				new_item['month'] = month_labels[new_item['month']]
		return new_data
	except Exception as e:
		raise e

def get_demand_per_meal_type_formatted_data(dataframe):
	new_data = []
	try:
		not_found = True
		for item in dataframe:
			for month in new_data:
				not_found = True
				if item['Date'] == month['Date']:
					not_found = False
					month[item["Type"]] = item['Forecast']
					break
			if not_found:
				data = {'Date':item['Date'], item["Type"]:item['Forecast']}
				new_data.append(data)
		return new_data
	except Exception as e:
		raise e

def get_month_label():
	month_labels = {
		1:"January",
		2:"February",
		3:"March",
		4:"April",
		5:"May",
		6:"June",
		7:"July",
		8:"August",
		9:"September",
		10:"October",
		11:"November",
		12:"December",
	}
	return month_labels