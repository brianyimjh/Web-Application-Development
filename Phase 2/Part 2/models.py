import pymongo
import json
from bson import json_util
from datetime import datetime, timedelta
from flask_login import UserMixin

connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['ECA_fitwell']

class User(UserMixin):
    def __init__(self, email, record):
        self._email = email
        self._record = record

    # For the Login Manager : Flask Login package
    def get_id(self):
        return self._email

    def get_record(self):
        return self._record

class FitwellUser():
    def __init__(self, email, password, gender, weight, height, date_of_birth):
        user = {
            'email': email,
            'password': password,
            'gender': gender,
            'weight': weight,
            'height': height,
            'date_of_birth': date_of_birth
        }

        db.users.insert_one(user)

    def get_user_byEmail(email):
        filter = {}
        filter['email'] = email

        aCursor = db.users.find(filter).limit(1)
        if aCursor.count() == 1:
            return User(email=email, record=aCursor.next())
        else:
            return None

class FitwellLog():
    def __init__(self, email, date_time, weight, walking_duration, running_duration, \
        swimming_duration, bicycling_duration, activity_calories_consumed):

        # Get user
        user = FitwellUser.get_user_byEmail(email).get_record()

        # Get age
        today = datetime.today()
        born = user['date_of_birth']
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        # Get date of log
        date = date_time.date()
        start_date = datetime(date.year, date.month, date.day)
        date_plus_one = date + timedelta(days=1)
        end_date = datetime(date_plus_one.year, date_plus_one.month, date_plus_one.day)

        current_log = FitwellLog.get_record_by_date(email, start_date, end_date)

        # Get height
        height = user['height']

        if current_log == None:
            if user['gender'] == 'M':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            elif user['gender'] == 'F':
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            daily_total_calories_consumed = 0
            daily_total_calories_consumed = bmr + activity_calories_consumed
        else:
            bmr = current_log['bmr']
            daily_total_calories_consumed = current_log['daily_total_calories_consumed']
            daily_total_calories_consumed += activity_calories_consumed

        log = {
            'email': email,
            'date_time': date_time,
            'weight': weight,
            'walking_duration': walking_duration,
            'running_duration': running_duration,
            'swimming_duration': swimming_duration,
            'bicycling_duration': bicycling_duration,
            'bmr': bmr,
            'activity_calories_consumed': activity_calories_consumed,
            'daily_total_calories_consumed': daily_total_calories_consumed
        }

        db.logs.insert_one(log)

    def get_record_by_date(email, start_date, end_date):
        filter = {
            'email': email,
            'date_time': {
                '$gte': start_date,
                '$lte': end_date
            },
        }

        record = db.logs.find_one(filter, sort=[('_id', pymongo.DESCENDING)])
        return record

    def calculate_activities_calories(weight, walking_duration, running_duration, \
        swimming_duration, bicycling_duration):
        walking_calorie_consumed = 0.084
        running_calorie_consumed = 0.21
        swimming_calorie_consumed = 0.13
        bicycling_calorie_consumed = 0.064

        activity_calories_consumed = (walking_calorie_consumed*walking_duration + \
        running_calorie_consumed*running_duration + \
        swimming_calorie_consumed*swimming_duration + \
        bicycling_calorie_consumed*bicycling_duration) * \
        weight

        return activity_calories_consumed

    def get_datetime_calories(email):
        collection = db["logs"]
        json_data = []

        if email == 'admin@fitwell.com':
            for record in collection.find():
                json_data.append({
                    'email': record['email'],
                    'date': record['date_time'].strftime("%Y-%m-%d"),
                    'value': record['daily_total_calories_consumed']
                })
        else:
            for record in collection.find({'email': email}):
                json_data.append({
                    'email': record['email'],
                    'date': record['date_time'].strftime("%Y-%m-%d"),
                    'value': record['daily_total_calories_consumed']
                })

        json_data = json.dumps(json_data, default=json_util.default)

        return json_data