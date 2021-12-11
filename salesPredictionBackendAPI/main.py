import traceback

from flask import Flask, jsonify, make_response, request, abort
import pandas as pd
import catboost
import pickle
from flask_cors import CORS, cross_origin
from google.cloud import pubsub_v1
import json
import os
from google.api_core import retry

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "civic-matrix-327917-eda1069fb875.json"

model = pickle.load(open("finalized_model.sav", "rb"))
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
request = None

# GCP topic, project & subscription ids
PUB_SUB_TOPIC = "product-pubsub"
PUB_SUB_PROJECT = "civic-matrix-327917"
PUB_SUB_SUBSCRIPTION = "product-ml"
final_dictionary = {}

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
    print("dataframe", df)
    cols = ["CONSOLE", "CATEGORY", "RATING", "YEAR", "USER_POINTS", "PUBLISHER", "CRITICS_POINTS"]
    df = df[cols]
    result = model.predict(df)[0]
    final_result = "<style>*{ box-sizing: border-box; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; } body{ font-family: Helvetica; -webkit-font-smoothing: antialiased; background: linear-gradient(#141e30, #243b55); } .table-wrapper{ margin: 10px 70px 70px; box-shadow: 0px 35px 50px rgba( 0, 0, 0, 0.2 ); } .fl-table { border-radius: 5px; font-size: 12px; font-weight: normal; border: none; border-collapse: collapse; width: 100%; max-width: 100%; white-space: nowrap; background-color: white; } .fl-table td, .fl-table th { text-align: center; padding: 8px; } .fl-table td { border-right: 1px solid #f8f8f8; font-size: 12px; } .fl-table thead th { color: #ffffff; background: #4FC3A1; } .fl-table thead th:nth-child(odd) { color: #ffffff; background: #324960; } .fl-table tr:nth-child(even) { background: #F8F8F8; } h2{ text-align: center; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; color: white; padding: 30px 0; }</style>" \
                   "<div class=\"table-wrapper\">" \
                   "<h2>Sales Prediction</h2>" \
                   "<table class=\"fl-table\">" \
                   "<tr> <th>CATEGORY</th> <th>CONSOLE</th> " \
                   "<th>PUBLISHER</th> <th>RATING</th> <th>USER_POINTS</th> " \
                   "<th>CRITICS_POINTS</th> <th>YEAR</th> <th>SALES PREDICTION</th> </tr> <tr> <td>" + str(
        final_dictionary.get("CATEGORY")) + "</td> <td>" + \
                   str(final_dictionary.get("CONSOLE")) + "</td> <td>" + str(
        final_dictionary.get("PUBLISHER")) + "</td> <td>" + str(final_dictionary.get("RATING")) \
                   + "</td> <td>" + str(final_dictionary.get("USER_POINTS")) + "</td> <td>" \
                   + str(final_dictionary.get("CRITICS_POINTS")) + "</td> <td>" + str(final_dictionary.get("YEAR")) \
                   + "</td> <td>" + str(result) + "</td> </tr> <table>" \
                                                  "</div>"
    print(final_result)
    return final_result, 200


def process_payload(message):
    global final_dictionary
    final_dictionary = json.loads(message.data)
    print(final_dictionary)
    message.ack()

@app.route("/get_prediction", methods=['GET', 'POST'])
@cross_origin()
def get_prediction():
    consume_payload()
    if not final_dictionary:
        abort(400)
    print("predict", final_dictionary)
    return result_data(final_dictionary)


# consumer function to consume messages from a topics for a given timeout period
# @app.route("/")
def consume_payload():
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PUB_SUB_PROJECT, PUB_SUB_SUBSCRIPTION)
        print(f"Listening for messages on {subscription_path}..\n")
        with subscriber:
            print("in subscriber")

            # The subscriber pulls a specific number of messages. The actual
            # number of messages pulled may be smaller than max_messages.
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 1},
                retry=retry.Retry(deadline=300),
            )
            ack_ids = []
            for received_message in response.received_messages:
                print(f"Received: {received_message.message.data}.")
                ack_ids.append(received_message.ack_id)

            # Acknowledges the received messages so they will not be sent again.
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
            print(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
            process_payload(response.received_messages[0].message)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    app.run("localhost", port=8090)
# app.run("localhost", port=8090)
