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
		new_df['Date'] = new_df['Date'].astype(str)
		print("stock_details=\n",new_df)
		return new_df
	except Exception as e:
		raise e

# get BOM details with filter
def get_bom_per_demand_with_filter(data, bom_details):
	try:
		bom_details['Date'] = pd.to_datetime(bom_details['Date'])
		item = data.get('item', '')
		date = data.get('date', '')
		
		query = ""
		if item != "":
			query+='Item.str.contains("'+item+'")'

		print("get_bom_per_demand_with_filter:query=",query)
		new_df = bom_details.query(query)
		new_df = new_df[new_df['Date'].dt.strftime('%d-%m-%Y') == date].astype(str)
		new_df['Date'] = new_df['Date'].astype(str)

		print("bom_details=\n",new_df)
		return new_df
	except Exception as e:
		raise e

# get demand per meal details with filter
def get_demand_per_meal_with_filter(data, sales_order_details):
	try:
		sales_order_details['Date'] = pd.to_datetime(sales_order_details['Date'])
		item = data.get('item', '')
		date = data.get('date', '')
		
		query = ""
		if item != "":
			query+='Item.str.contains("'+item+'")'

		print("get_demand_per_meal_with_filter:query=",query)
		group_by_item_df = sales_order_details.query(query)
		print("group_by_item_df=\n",group_by_item_df)
		final_df = group_by_item_df[group_by_item_df['Date'].dt.strftime('%d-%m-%Y') == date].astype(str)
		# final_df = pd.DataFrame(final_df['Date'],final_df['Item'],final_df['forecast'])
		print("final_df=\n",final_df)
		return final_df
	except Exception as e:
		raise e


# get demand per meal details with filter
def get_all_demand_per_meal(sales_order_details):
	try:
		sales_order_details['Date'] = pd.to_datetime(sales_order_details['Date'])
		final_df = sales_order_details.groupby('Item')
		print("group_by_item_df=\n",final_df)
		print("final_df=\n",final_df)
		return final_df
	except Exception as e:
		raise e