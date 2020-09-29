import json
from typing import List, Dict

from bson import ObjectId
from flask import Flask, request
from flask_cors import CORS
from pymongo.cursor import Cursor

from events.event_type_mapping import EventMaker, EVENT_TYPE_MAPPING
from mongo.db_client import MongoDBClient


app = Flask(__name__)
cors = CORS(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def _encode_data(cursor: [Cursor, List]) -> Dict:
    requested_persons = {"data": []}
    for element in cursor:
        requested_persons["data"].append(element)
    return JSONEncoder().encode(requested_persons)


@app.route('/')
def hello_world():
    return "Hello, World!"


@app.route("/person/<army_id>")
def show_person(army_id):
    db_client = MongoDBClient()
    person_info = db_client.find_in_collection("persons", {"army_id": army_id})[0]

    events = {}
    for event_type in EVENT_TYPE_MAPPING.keys():
        events[event_type] = list(db_client.find_in_collection(event_type, {"army_id": army_id}))
    print(events)

    person_data = {"info": person_info, "events": events}

    return person_data


@app.route("/person", methods=["POST"])
def register_persons():
    if request.method == "POST":
        persons: List = request.json

        db_client = MongoDBClient()
        db_client.insert_document(persons, "persons")

        return _encode_data(persons)


@app.route("/event/<event_type>", methods=["POST", "GET"])
def update_event(event_type):
    if request.method == "POST":
        scores: List = request.json

        event = EventMaker(event_type).make_event()
        event.add_scores(scores)
        scores = event.publish_scores()

        db_client = MongoDBClient()
        db_client.insert_document(scores, event_type)

        return _encode_data(scores)
    if request.method == "GET":
        db_client = MongoDBClient()
        scores = db_client.find_in_collection(event_type, {})
        data = {"scores": [score for score in scores]}
        return data


if __name__ == '__main__':
    app.run()
