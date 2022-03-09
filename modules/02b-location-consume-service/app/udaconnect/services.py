import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import session
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-consume")


class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location(
            person_id=location["person_id"],
            creation_time=location["creation_time"],
            coordinate=ST_Point(location["latitude"], location["longitude"])
        )
        session.add(new_location)
        session.commit()
        session.flush()
        print("new location stored at id:", new_location.id)
        return
