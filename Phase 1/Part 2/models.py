import pymongo
import json
from bson import json_util

connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['TMA01_fitwell']

class FitwellLog():
    def __init__(self, date_time, weight, walking_duration, running_duration, swimming_duration, bicycling_duration, total_calories_consumed):
        # Create a record in the database using insert_one
        db.logs.insert_one({
            'date_time': date_time,
            'weight': weight,
            'walking_duration': walking_duration,
            'running_duration': running_duration,
            'swimming_duration': swimming_duration,
            'bicycling_duration': bicycling_duration,
            'total_calories_consumed': total_calories_consumed
        })

class FitwellUpload():
    def __init__(self, email, date_time, weight, walking_duration, running_duration, swimming_duration, bicycling_duration, total_calories_consumed):
        # Create a record in the database using insert_one
        db.uploads.insert_one({
            'email': email,
            'date_time': date_time,
            'weight': weight,
            'walking_duration': walking_duration,
            'running_duration': running_duration,
            'swimming_duration': swimming_duration,
            'bicycling_duration': bicycling_duration,
            'total_calories_consumed': total_calories_consumed
        })

    def get_datetime_calories():
        collection = db["uploads"]
        json_data = []

        for record in collection.find():
            json_data.append({
                'date': record['date_time'].strftime("%Y-%m-%d"),
                'value': record['total_calories_consumed']
            })

        json_data = json.dumps(json_data, default=json_util.default)

        return json_data