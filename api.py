
from flask import Flask, jsonify

from sklearn.externals import joblib


app = Flask(__name__)

model_directory = '.'
model_file_name = '%s/model.pkl' % model_directory

@app.route('/api/taxi_price/predict')
def predict():
    return jsonify({ 'prediction': 250 })

if __name__ == '__main__':
    try:
        reg = joblib.load(model_file_name)
        print('model loaded')
    except Exception as e:
        print('No model here')

    app.run(host='0.0.0.0', port=4000, debug=True)

