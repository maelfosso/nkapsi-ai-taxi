
from flask import Flask, jsonify
import googlemaps
import requests
import json
from sklearn.externals import joblib


app = Flask(__name__)

api_key = "AIzaSyDa6owoMnnd3p7uCd_V9Lc3v2BbzhI6xSY"
gmaps = googlemaps.Client(key=api_key)

base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

model_directory = '.'
model_file_name = '%s/model.pkl' % model_directory

@app.route('/api/predict/taxi_price/<origins>/<destinations>', methods=['GET'])
def predict(origins, destinations):
    # Get parameters
    # print(origins)
    # print(destinations)

    # Construct the payload
    payload = {
        'origins': origins, # '3.862905, 11.496651',
        'destinations': destinations, # '3.872068, 11.511543',
		'mode' : 'driving',
        'api_key': api_key
    }

    # Calculate directions
    # results = gmaps.distance_matrix(origins, destinations, mode='driving')
    results = gmaps.directions(origins, destinations, mode='driving')
    print(results)
    result = results[0]
    result = result["legs"][0]
    print(result)

    start_address = result["start_address"]
    start_location = result["start_location"]
    end_address = result["end_address"]
    end_location = result["end_location"]
    steps = result["steps"]
    distance = result["distance"]

    print()
    print(json.dumps(start_location))
    print(json.dumps(start_address))
    print()
    print(json.dumps(end_location))
    print(json.dumps(end_address))
    print()
    print(len(steps))
    print()
    print(distance)

    # Get meters and virage between origins and destinations
    turn = len(steps)
    distance = distance["value"]

    # Predict price
    # query = {
    #     'distance': int(distance),
    #     'turn': int(turn)
    # }
    query = [int(distance), int(turn)]
    prediction = model.predict([query])[0]
    print()
    print("RESULT PREDICT IS : %s" %(prediction))

    return jsonify({
        'end_address': end_address,
        # 'end_location': end_location,
        'start_address': start_address,
        # 'start_location': start_location,
        'distance': int(distance),
        'turn': len(steps),
        'prediction': prediction
    })

if __name__ == '__main__':

    model = joblib.load(model_file_name)

    # try:
    #     reg = joblib.load(model_file_name)
    #     print('model loaded')
    # except Exception as e:
    #     print('No model here')

    app.run(host='0.0.0.0', port=4000, debug=True)
