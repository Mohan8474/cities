#!/usr/bin/env python3
import os
import sys
import json
from flask import current_app

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parentdir)
sys.path.insert(0, parentdir)


from app.models import db, Cities


file_path = os.path.join(os.path.dirname(__file__), "cities.json")

with open(file_path, "r") as file:
    json_data = json.load(file)



def load_data():
    for cities in json_data:
        cities_data = Cities(
            name=cities["name"],
            country=cities["country"],
            lat=cities["lat"],
            lng=cities["lng"],
        )
        db.session.add(cities_data)
    db.session.commit()


load_data()
