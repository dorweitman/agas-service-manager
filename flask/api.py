import json
import os
from datetime import timedelta, datetime
from typing import List, Dict

import pandas as pd
from bson import ObjectId
from flask import Flask, request
from flask_cors import CORS
from pymongo.cursor import Cursor

from events.event_type_mapping import EventMaker, EVENT_TYPE_MAPPING
from match.neighbores_finder import map_person_to_matches, RunScore
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

    person_data = {"info": person_info, "events": events}

    return person_data


@app.route("/community/<army_id>")
def find_partners(army_id):
    db_client = MongoDBClient()
    scores = list(db_client.find_in_collection("run", {}))
    possible_matches_scores = []
    for score in scores:
        army_id = score["army_id"]
        duration = score["duration_in_minutes"]
        possible_matches_scores.append(RunScore(army_id, duration))

    person_to_matches = map_person_to_matches(possible_matches_scores)
    matches: List[RunScore] = person_to_matches[army_id]
    results = []
    for match in matches:
        matching_person = db_client.find_one_in_collection("persons", {"army_id": match.army_id})
        name = matching_person["name"]
        phone = matching_person["phone"]
        duration = str((datetime.min + timedelta(seconds=match.duration * 60)).time())
        results.append({"name": name, "duration": duration, "phone": phone})
    return {"matches": results}


@app.route("/person", methods=["POST"])
def register_persons():
    if request.method == "POST":
        persons: List = request.json
        for person in persons:
            person["name"] = f"{person['first_name']} {person['last_name']}"
            person.pop("first_name", None)
            person.pop("last_name", None)
            person["army_id"] = str(person["army_id"])

        db_client = MongoDBClient()
        db_client.insert_documents(persons, "persons")

        for person in persons:
            person.pop("_id", None)

        return {"persons": persons}


@app.route("/event/<event_type>", methods=["POST", "GET"])
def update_event(event_type):
    if request.method == "POST":
        scores: List = request.json

        event = EventMaker(event_type).make_event()
        event.add_scores(scores)
        scores = event.publish_scores()

        db_client = MongoDBClient()
        db_client.insert_documents(scores, event_type)

        return _encode_data(scores)
    if request.method == "GET":
        db_client = MongoDBClient()
        scores = db_client.find_in_collection(event_type, {})
        data = {"scores": [score for score in scores]}
        return data


@app.route("/export/event/<event_type>")
def export_scheme(event_type):
    name = request.args.get("name", "")
    date = request.args.get("date", "")

    db_client = MongoDBClient()
    table = list(db_client.find_in_collection(event_type, {"name": name, "date": date}))
    df = pd.DataFrame(table)

    directory = os.path.expanduser("~/Downloads")
    file = f"{event_type}_{name}_{date}.xlsx"

    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_excel(os.path.join(directory, file))

    return df.to_dict()


@app.route("/search")
def search_event():
    search = request.args.get("search", "")
    search = f"\"" + search + f"\""

    db_client = MongoDBClient()
    collections_names = db_client.db.list_collection_names()

    results = {}
    for collection_name in collections_names:
        results[collection_name] = list(db_client.find_in_collection(collection_name, {"$text": {"$search": search}}))

    return results


if __name__ == '__main__':
    app.run()
