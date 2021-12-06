from flask import Flask, jsonify, make_response, request, abort
import pandas as pd
import catboost
import pickle
from flask_cors import CORS, cross_origin
from google.cloud import pubsub_v1
import json
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="civic-matrix-327917-eda1069fb875.json"



model = pickle.load(open("finalized_model.sav", "rb"))
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
request = None

# GCP topic, project & subscription ids
PUB_SUB_TOPIC = "product-pubsub"
PUB_SUB_PROJECT = "civic-matrix-327917"
PUB_SUB_SUBSCRIPTION = "product-ml"
final_dictionary = None

project = PUB_SUB_PROJECT
subscription = PUB_SUB_SUBSCRIPTION


# Pub/Sub consumer timeout
period = 3.0

@app.errorhandler(404)

@app.route("/fetch")
def fetch_details():
    return "From App Engine!"


def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



def result_data(final_dictionary):
    df = pd.DataFrame(final_dictionary, index=[0])
    print("dataframe",df)
    cols=["YEAR","CATEGORY","CONSOLE","PUBLISHER","RATING","CRITICS_POINTS","USER_POINTS"]
    df = df[cols] 
    return jsonify({'result': model.predict(df)[0]})
   

def process_payload(message):
    global final_dictionary
    final_dictionary = json.loads(message.data)
    print(final_dictionary)
    message.ack()      

@app.route("/get_prediction", methods=['GET','POST'])
@cross_origin()
def get_prediction():
    if not final_dictionary:
        abort(400)    
    print("predict",final_dictionary)
    return result_data(final_dictionary)
   
    

# consumer function to consume messages from a topics for a given timeout period
@app.route("/")
def consume_payload():
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT, PUB_SUB_SUBSCRIPTION)
        print(f"Listening for messages on {subscription_path}..\n")
        streaming_pull_future = subscriber.subscribe(subscription_path,callback=process_payload)
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.                
                streaming_pull_future.result()

            except TimeoutError:
                streaming_pull_future.cancel()
     

if __name__ == "__main__":
  app.run(host='127.0.0.1', port=8080, debug=True)