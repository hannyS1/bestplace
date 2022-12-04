import sys
import csv
import ast
from typing import List

import h3

from config.database import SessionLocal
from core.entities import ApartmentBuilding
from core.utils.h3 import H3Constants


def main():
    filename = sys.argv[1]
    buildings: List[ApartmentBuilding] = []
    with open(filename, newline="") as file:
        reader = csv.DictReader(file, delimiter=",")
        for row in reader:
            geopos_dict = ast.literal_eval(row["geopos"])
            coordinates = geopos_dict.get("coordinates")
            longitude = coordinates[0]
            latitude = coordinates[1]
            h3_value = h3.geo_to_h3(latitude, longitude, resolution=H3Constants.RESOLUTION)
            buildings.append(
                ApartmentBuilding(
                    id=int(row.get("id")),
                    apartments_count=int(row.get("apartments")),
                    price=float(row.get("price")),
                    year=int(row.get("year")),
                    longitude=longitude,
                    latitude=latitude,
                    h3_value=h3_value,
                )
            )
    session = SessionLocal()
    session.query(ApartmentBuilding).delete()
    session.bulk_save_objects(buildings)
    session.commit()


if __name__ == "__main__":
    main()
