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
	# path = "C:/Users/balac/Downloads/SaudiCaterers Data template-V1.xlsx"
	# sales_order_details = pd.read_excel(path,sheet_name='Sales-Order details')
	# sales_order_details['Date'] = pd.to_datetime(sales_order_details['Date'])
	# totalSum = pd.DataFrame(sales_order_details.groupby([sales_order_details['Date'].dt.month,'Item category'])['orders'].sum().reset_index(name='orders'))
	# final_df = totalSum.rename(columns={'Date': 'month'})
	# dataframe = json.loads(final_df.to_json(orient="records"))
	# print("dataframe=\n",dataframe)
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
				data = {'month':item['month'], item["Item category"]:item['orders']}
				new_data.append(data)
		# update month to text label
		field_key = 'month'
		for new_item in new_data:
			if field_key in new_item:
				new_item['month'] = month_labels[new_item['month']]
		print("new_data=\n",new_data)
		return new_data
	except Exception as e:
		raise e

def get_demand_per_meal_type_formatted_data(dataframe):
	# path = "C:/Users/balac/Downloads/SaudiCaterers Data template-V1.xlsx"
	# demand_per_meal_type = pd.read_excel(path,sheet_name='Demand per meal type')
	# demand_per_meal_type['Date'] = pd.to_datetime(demand_per_meal_type['Date'])
	# totalSum = pd.DataFrame(demand_per_meal_type.groupby([demand_per_meal_type['Date'],'Type'])['Forecast'].sum().reset_index(name='Forecast'))
	# totalSum['Date'] = totalSum['Date'].astype(str)
	# dataframe = json.loads(totalSum.to_json(orient="records"))
	# print("dataframe=\n",dataframe)
	# month_labels = get_month_label()
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
		print("new_data=\n",new_data)
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

# get_demand_per_meal_type_formatted_data()
# get_meals_monthly_formatted_data()