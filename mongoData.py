# For handling the database!
from datetime import datetime, timedelta
from pymongo import MongoClient
import pymongo

class MongoDBRepo:
    def date_formatted(date):
        return date.strftime('%d %b %H:%M')
    def get_data(self, topic_name, numRecords):
        mongoClient = MongoClient()
        db=mongoClient.SensorData
        # Currently gets all data from the beginning of time
        cursor = db.enose_data.find({"topic":topic_name}).limit(numRecords)
        values = []
        labels=[]
        for element in cursor:
            values.append(element['value'])
            labels.append(element['time'])
        return labels, values

    def get_latest_data(self, topics):
        mongoClient = MongoClient()
        db=mongoClient.SensorData
        values = []
        for topic in topics:
            cursor = db.enose_data.find({"topic":topic}).sort("time",pymongo.DESCENDING).limit(1)
            # Latest values!
            values.append(cursor[0]['value'])
        return values
        