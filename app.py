from flask import Flask, request, jsonify, send_from_directory,json,Response
from werkzeug.utils import secure_filename
from flasgger import Swagger
import os
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd
from werkzeug.serving import run_simple
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from commons import get_uuid, get_avg_flight_intime
from sales_filter import get_sales_data, get_meals_per_destination_with_filter
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# logging config
handler = RotatingFileHandler('static/logs/middleware.log', maxBytes=1)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
handler.setFormatter(formatter)
logging.getLogger('').setLevel(logging.DEBUG)
logging.getLogger('').addHandler(handler)

# swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'File data API Application'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("PATH=",path)
        file.save(path)

        global sales_order_details
        global palnned_flights
        global seasonality
        global trend
        global Sheet1

        sales_order_details = pd.read_excel(path,sheet_name='Sales-Order details')
        palnned_flights = pd.read_excel(path,sheet_name='Palnned flights')
        seasonality = pd.read_excel(path,sheet_name='seasonality')
        trend = pd.read_excel(path,sheet_name='trend')
        Sheet1 = pd.read_excel(path,sheet_name='Sheet1')

        return jsonify({"message": "File uploaded successfully", "filename": filename, "data":""}), 200
    else:
        return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

@app.route('/sales', methods=['POST'])    
@cross_origin()
def sales():
    logging.info('/sales....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:UUID:="+str(uid)+" <<<-----<<")
    data = json.loads(request.data)
    # REQUEST BODY
    print(data)
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400
        data = get_sales_data(data, sales_order_details)
        return Response(data , mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:sales="+e)

@app.route('/seasonality', methods=['GET'])    
@cross_origin()
def seasonality():
    logging.info('/seasonality....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:seasonality:UUID:="+str(uid)+" <<<-----<<")
    try:
        global seasonality
        if 'seasonality' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        month = seasonality.month
        Seasonality = seasonality.Seasonality
        dataset = pd.DataFrame({'month': month, 'seasonality': Seasonality})
        dataframe = json.loads(dataset.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:seasonality="+e)


@app.route('/trend', methods=['GET'])    
@cross_origin()
def trend():
    logging.info('/trend....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:TREND:UUID:="+str(uid)+" <<<-----<<")
    try:
        global trend
        if 'trend' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400
        
        month = trend.date
        trend_data = trend.Trend
        dataset = pd.DataFrame({'date': month.astype(str), 'trend': trend_data})
        dataframe = json.loads(dataset.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:trend="+e)

@app.route('/getAllSales', methods=['GET'])    
@cross_origin()
def getAllSales():
    logging.info('/getAllSales....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getAllSales:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        dataframe = json.loads(sales_order_details.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getAllSales="+e)


@app.route('/getAverageMealsServed', methods=['GET'])    
@cross_origin()
def getAverageMealsServed():
    logging.info('/getAverageMealsServed....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getAverageMealsServed:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400
        total_records = len(sales_order_details)
        print(total_records)
        total_orders = sales_order_details['orders'].sum()
        data = {
          "average_orders": total_orders//total_records
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getAverageMealsServed="+e)


@app.route('/getAllRoutes', methods=['GET'])    
@cross_origin()
def getAllRoutes():
    logging.info('/getAllRoutes....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getAllRoutes:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        df2 = sales_order_details.groupby(['Route','Latitude','Longitude']).size().reset_index(name='Count')
        dataframe = json.loads(df2.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getAllRoutes="+e)

@app.route('/getMealCatStats', methods=['GET'])    
@cross_origin()
def getMealCatStats():
    logging.info('/getMealCatStats....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getMealCatStats:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        df2 = sales_order_details.groupby(['Item category']).size().reset_index(name='Count')
        dataframe = json.loads(df2.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getMealCatStats="+e)


@app.route('/getCostOfOrdersPlaces', methods=['GET'])    
@cross_origin()
def getCostOfOrdersPlaces():
    logging.info('/getCostOfOrdersPlaces....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getCostOfOrdersPlaces:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        total_cost_per_day = sales_order_details['cost per order'].sum()
        data = {
          "total_cost_per_day": total_cost_per_day
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getCostOfOrdersPlaces="+e)


@app.route('/getMealsMonthly', methods=['GET'])    
@cross_origin()
def getMealsMonthly():
    logging.info('/getMealsMonthly....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getMealsMonthly:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400
    
        # sales_order_details['Date'] = pd.to_datetime(sales_order_details['Date'])
        # totalSum = sales_order_details.groupby([pd.to_datetime(sales_order_details['Date']).dt.month, 'Date']).agg({'orders': sum})
        sales_order_details['Date'] = pd.to_datetime(sales_order_details['Date'])
        # totalSum = sales_order_details.groupby(sales_order_details['Date'].dt.month)['orders'].sum().reset_index(name='orders')
        totalSum = pd.DataFrame(sales_order_details.groupby([sales_order_details['Date'].dt.month,'Item category'])['orders'].sum().reset_index(name='orders'))
        print("totalSum=\n",totalSum)
        final_df = totalSum.rename(columns={'Date': 'month'})
        print(final_df)
        dataframe = json.loads(final_df.to_json(orient="records"))
        data = {
          "data": dataframe,
          # "data": dataframe2
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getMealsMonthly="+e)


@app.route('/getMealsPerDestinatin', methods=['GET'])    
@cross_origin()
def getMealsPerDestinatin():
    logging.info('/getMealsPerDestinatin....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getMealsPerDestinatin:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400
    
        total_orders = sales_order_details.groupby('Arrival location')['orders'].sum().reset_index(name='orders')
        dataframe = json.loads(total_orders.to_json(orient="records"))
        data = {
          "data": dataframe
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getMealsPerDestinatin="+e)


@app.route('/getAvgFlightInTime', methods=['GET'])    
@cross_origin()
def getAvgFlightInTime():
    logging.info('/getAvgFlightInTime....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getAvgFlightInTime:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        final_df, average_flight_in_time = get_avg_flight_intime(sales_order_details)
        dataframe = json.loads(final_df.to_json(orient="records"))
        # average_flight_in_time = json.loads(average_flight_in_time.to_json(orient="records"))
        data = {
          # "data": dataframe,
          "avg_flight_in_time": str( average_flight_in_time)
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getAvgFlightInTime="+e)

@app.route('/getMaxOrdersPlacedTime', methods=['GET'])    
@cross_origin()
def getMaxOrdersPlacedTime():
    logging.info('/getMaxOrdersPlacedTime....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getMaxOrdersPlacedTime:UUID:="+str(uid)+" <<<-----<<")
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        total_orders = sales_order_details.groupby(['Flight Number','Latitude','Longitude','Route','Date','Arrival Time','Departure time','Arrival location'])['orders'].sum().reset_index().max()
        print(total_orders)
        dataframe = json.loads(total_orders.to_json(orient="records"))
        # average_flight_in_time = json.loads(average_flight_in_time.to_json(orient="records"))
        data = {
          "data": {
          "flight": total_orders[0],
          "Latitude": total_orders[1],
          "Longitude": total_orders[2],
          "Route": total_orders[3],
          "Date": str(total_orders[4]),
          "Arrival": str(total_orders[5]),
          "Departure": str(total_orders[6]),
          # "Arrival_location": total_orders[7],
          "orders": total_orders[8]
          }
        }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getMaxOrdersPlacedTime="+e)

@app.route('/getMealsPerDestinationFilter', methods=['POST'])    
@cross_origin()
def getMealsPerDestinationFilter():
    logging.info('/getMealsPerDestinationFilter....')
    cur_datetime, uid = get_uuid()
    logging.info(">>----->>> START:getMealsPerDestinationFilter:UUID:="+str(uid)+" <<<-----<<")
    data = json.loads(request.data)
    print(data)
    try:
        global sales_order_details
        if 'sales_order_details' not in globals():
            return jsonify({"message": "No CSV file uploaded"}), 400

        data = get_meals_per_destination_with_filter(data, sales_order_details)
        total_orders = data.groupby('Arrival location')['orders'].sum().reset_index(name='orders')
        final_data = json.dumps(json.loads(total_orders.to_json(orient="records")))
        print("data=\n",total_orders)
        return Response(final_data , mimetype='application/json')
    except Exception as e:
        print(e)
        logging.debug("Xception:getMealsPerDestinationFilter="+e)

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)    
    logging.info('Started')
    print('Server Started at http://127.0.0.1:5001')
    # app.run(host='127.0.0.1', port=5001,debug=True, threaded=True)
    run_simple('127.0.0.1', 5001, app)
