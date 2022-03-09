import logging
import datetime
import json
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from flask import jsonify
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-process-api")

producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092')
topic_location = "locations"


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        #new_location = Location()
        #new_location.person_id = location["person_id"]
        #new_location.creation_time = location["creation_time"]
        #new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        #db.session.add(new_location)
        #db.session.commit()

        new_location = {}
        new_location["person_id"] = location["person_id"]
        new_location["creation_time"] = datetime.datetime.now().isoformat()
        new_location["latitude"] = location["latitude"]
        new_location["longitude"] = location["longitude"]
        #new_location["coordinate"] = ST_Point(location["latitude"], location["longitude"])

        # Write to Kafka topic
        producer.send(topic_location, value=json.dumps(new_location).encode())

        return jsonify({"status": "OK"})
