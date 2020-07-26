import time
import random
from collections import deque
from pandas_datareader.data import DataReader
import datetime
import sys
from flask import Flask, render_template, request, jsonify, send_file
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json
import csv

from pymongo import MongoClient
import mongoData

# MQTT SETUP
server = Flask(__name__)

server.config['MQTT_BROKER_URL'] = 'enose.ga'
server.config['MQTT_BROKER_PORT'] = 1884
server.config['MQTT_USERNAME'] = '' # Removed for security purposes!
server.config['MQTT_PASSWORD'] = '' # Removed for security purposes!
server.config['MQTT_REFRESH_TIME'] = 1.0

mqtt = Mqtt(server)
socketio = SocketIO(server)

# Database
mongoClient = MongoClient()
db=mongoClient.SensorData
collection=db.enose_data
repo = mongoData.MongoDBRepo

@server.route("/")
def main():
  return render_template('/index.html')

@server.route("/enoseSimulator")
def sim():
    return render_template('simulator.html')

@server.route("/graphing")
def graphs():
    return render_template('/chart.html')

@server.route("/datarecorder")
def recorder():
    return render_template('/recorder.html')

@server.route('/return-files/')
def return_files_tut():
	try:
		return send_file('test.csv', as_attachment=True, cache_timeout=0, attachment_filename='data.csv')
	except Exception as e:
		return str(e)




# API to get data
@server.route('/ChartData/api/<string:sensor>')
def get_measurements_as_labels_and_values(sensor):
    numRecords = request.args.get('numRecords', default=10, type=int)
    print("Got request of", request.args.get('numRecords'))
    topic = sensor
    labels, values = update_enose_values(topic, numRecords)

    return jsonify({"measurements":{'labels':labels,'values':values}})


# Subsribe to the MQTT topic the ESP32 is sending messages on
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('mics')
    mqtt.subscribe('temperature')
    mqtt.subscribe('pressure')
    mqtt.subscribe('humidity')
    mqtt.subscribe('CCS_eCO2')
    mqtt.subscribe('CCS_TVOC')
    mqtt.subscribe('SGP_TVOC')
    mqtt.subscribe('SGP_eCO2')
    mqtt.subscribe('SGP_H2')
    mqtt.subscribe('SGP_Ethanol')
    mqtt.subscribe('mox1')
    mqtt.subscribe('mox2')
    mqtt.subscribe('mox3')

    # To make data recording easier:
    mqtt.subscribe('new')
    mqtt.subscribe('enose')



@mqtt.on_message()

def handle_mqtt_message(client, userdata, message):
    start = time.time()
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    #print(data)
    # emit a mqtt_message event to the socket containing the message data
    print("Socket test!")
    socketio.emit('mqtt_message', data=data)

    receiveTime = time.strftime("%d/%m/%Y-%H:%M:%S")

    # Uncomment to use website for data recording application as ESP32 will transmit data in JSON format. 

    # print(json_parsed['mox1'])
    # For data recording:
    print(data['topic'])
    with open('test.csv','a+') as f:
        if(data['topic'] == "new"):
            print("NEW FILE!!")
            f.write("\n\n\nNEW EXPERIMENT \n\n\n")
            f.write('time,mox1,mox2,mox3,moxtemp,mics,bmetemp,bmehumidity,ccsTVOC,abshumid,sgpTVOC,sgpRawEthanol,sgpRawH2' + "\n")
        else:
            json_parsed = json.loads(data['payload'])
            f.write(str(receiveTime) + "," + 
            json_parsed['mox1'] + "," +
            json_parsed['mox2'] + ","+
            json_parsed['mox3'] + ","+
            json_parsed['moxtemp'] + ","+
            json_parsed['mics'] + ","+
            json_parsed['bmetemp'] + ","+
            json_parsed['bmehumidity'] + ","+
            json_parsed['ccsTVOC'] + ","+
            json_parsed['abshumid'] + ","+
            json_parsed['sgpTVOC'] + ","+
            json_parsed['sgpRawEthanol'] + ","+
            json_parsed['sgpRawH2'] + "\n")
        

    

    
    # # Add data to the database
    # isFloatValue = False
    # try:
    #     val = float(data['payload'])
    #     isFloatValue=True
    # except:
    #     isFloatValue=False

    # if(isFloatValue):
    #     receiveTime = datetime.datetime.now()
    #     print(str(receiveTime) + ": " + data['topic'] + " " + str(val))
    #     post={"time":receiveTime, "topic":data['topic'], "value":val}
    # else:
    #     print("Was not a float value!!")
    # collection.insert_one(post)

    # latestPredictors = repo.get_latest_data(repo,["mox1","mox2","mox3","humidity"])
    # print(latestPredictors)
    # latestPredictors = neural_preprocess(latestPredictors[0],latestPredictors[1],latestPredictors[2],latestPredictors[3])
    # # Perform ML prediction on latestPredictors! These are the values which were last input into the database.

    # prediction = neural_predict(neural_model, latestPredictors)
    # end = time.time()
    # print(end-start)
    # print(prediction)
    # # Performa action as a result of the neural prediction.
    # if(prediction == [0]):
    #     print("Urine not Detected!")
    #     urine_noAlert()
    # else:
    #     print("Urine Detected!")
    #     urine_alert()


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

    
socketio.run(server, host='localhost', port=5000, use_reloader=True, debug=True)

if __name__ == "__main__":
  server.run()
          