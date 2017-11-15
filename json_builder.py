import requests
import json

info = {
    'user': 16,
    "1": {
        "movie 8": 2.105974175224151,
        "movie 12": 2.846541428086288,
        "movie 24": 3.7335608311543287
    },
    "2": {
        "movie 24": 3.7335608311543287
    }
}

url = "https://cit-home1.herokuapp.com/api/rs_homework_1"

headers = {'Content-Type': 'application/json'}

r = requests.post(url, data=json.dumps(info), headers = headers)

print(r.json())

