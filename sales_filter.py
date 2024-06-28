import pandas as pd
from flask import json

def get_sales_data(data, sales_order_details):
	try:
		# Filter 1
		# {
		#   "route": "AB2",
		#   "career": "Saudia",
		#   "date": "01-01-2024",
		#   "time": "12:15:00",
		#   "meal_category": "Veg",
		#   "meal_type": "Pre-order",
		#   "meal": "Salmon-Rice meal",
		#   "passenger_class": ""
		# }

		# Filter 2
		# {
		#   "route": "Jeddah to Riyadh",
		#   "carrier": "Saudi Airlines",
		#   "date": "01-01-2024",
		#   "time": "12:15:00",
		#   "meal_category": "Non-Veg",
		#   "meal_type": "Pre-order",
		#   "meal": "Chicken Biriyani",
		#   "passenger_class": "Business"
		# }		
		route = data.get('route', '')
		Carrier = data.get('carrier', '')
		date = data.get('date', '')
		time = data.get('time', '')
		meal_category = data.get('meal_category', '')
		meal_type = data.get('meal_type', '')
		meal = data.get('meal', '')
		passenger_class = data.get('passenger_class', '')

		query = ""
		if route != "":
			query+='Route.str.contains("'+route+'")'
		if Carrier != "":
			query+=' & Carrier.str.contains("'+Carrier+'")'
		# if date != "":
		# 	query+=' & Date.str.conains("'+date+'")'
		# if time != "":
		# 	query+=' & Time.str.conains("'+time+'")'
		if meal != "":
			query+=' & Item.str.contains("'+meal+'")'
		if meal_category != "":
			query+=' & `Item category`.str.contains("'+meal_category+'")'
		if meal_type != "":
			query+=' & `Item type`.str.contains("'+meal_type+'")'
		if passenger_class != "":
			query+=' & `passenger class`.str.contains("'+passenger_class+'")'

		if query.startswith(" & "):
			print("query startswith  & ")
			query = query[3:]
		print(query)

		new_df = sales_order_details.query(query)
		final_data = json.dumps(json.loads(new_df.to_json(orient="records")))
		return final_data
	except Exception as e:
		raise e

def get_meals_per_destination_with_filter(data, sales_order_details):
	try:	
		route = data.get('route', '')
		Carrier = data.get('carrier', '')
		date = data.get('date', '')
		time = data.get('time', '')
		meal_category = data.get('meal_category', '')
		meal_type = data.get('meal_type', '')
		meal = data.get('meal', '')
		passenger_class = data.get('passenger_class', '')

		query = ""
		if route != "":
			query+='Route.str.contains("'+route+'")'
		if Carrier != "":
			query+=' & Carrier.str.contains("'+Carrier+'")'
		# if date != "":
		# 	query+=' & Date.str.conains("'+date+'")'
		# if time != "":
		# 	query+=' & Time.str.conains("'+time+'")'
		if meal != "":
			query+=' & Item.str.contains("'+meal+'")'
		if meal_category != "":
			query+=' & `Item category`.str.contains("'+meal_category+'")'
		if meal_type != "":
			query+=' & `Item type`.str.contains("'+meal_type+'")'
		if passenger_class != "":
			query+=' & `passenger class`.str.contains("'+passenger_class+'")'
		
		if query.startswith(" & "):
			print("query startswith  & ")
			query = query[3:]
		print("get_meals_per_destination_with_filter:query=",query)

		new_df = sales_order_details.query(query)
		return new_df
	except Exception as e:
		raise e

# get stock details with filter
def get_stock_details_with_filter(data, stock_details):
	try:
		item = data.get('item', '')
		query = ""
		if item != "":
			query+='Item.str.contains("'+item+'")'
		print("get_stock_details_with_filter:query=",query)
		new_df = stock_details.query(query)
		print("stock_details=\n",new_df)
		return new_df
	except Exception as e:
		raise e

# get BOM details with filter
def get_bom_per_demand_with_filter(data, bom_details):
	try:
		item = data.get('item', '')
		query = ""
		if item != "":
			query+='Item.str.contains("'+item+'")'
		print("get_bom_per_demand_with_filter:query=",query)
		new_df = bom_details.query(query)
		print("bom_details=\n",new_df)
		return new_df
	except Exception as e:
		raise e