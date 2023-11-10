import json
import csv
from datetime import datetime
from utils.time_to_store_status import store_status
from utils.text_to_number import convert_congestion

MAXSPEED = {
    "secondary": 44,
    "tertiary": 36,
    "trunk_link": 50,
    "trunk": 80,
    "primary": 49,
    "primary_link": 47,
}


def JsonToCSV():
    with open("newjsonfiles/congestions.json", "r") as f:
        data = json.load(f)

    osm_id_list = []

    FINAL = []
    for line in data:
        timest = str(line["Timestamp"].replace(":00.000", ""))
        div = timest.split()

        weekday = datetime.strptime(div[0], "%Y-%m-%d").strftime("%A").upper()
        time = div[1]
        stores = store_status(time=time, day=weekday)
        congestion = convert_congestion(str(line["Congestion"]))
        osm_id = str(line["Link_id"])

        FINAL.append(
            {
                "TIME": time,
                "DAY": weekday,
                "STORES": stores,
                "CONGESTION": congestion,
                "OSM_ID": osm_id,
            }
        )

    with open("newjsonfiles/filtered_osm.json", "r") as f:
        osm_data = json.load(f)

    for row in FINAL:
        if row["OSM_ID"] not in osm_id_list:
            osm_id_list.append(row["OSM_ID"])
            road_data = osm_data.get(row["OSM_ID"], None)
            length = (
                road_data.get("length", "unknown")
                if road_data is not None
                else "unknown"
            )
            row["ROAD_LENGTH_M"] = length
            for row1 in FINAL:
                if row1["OSM_ID"] == row["OSM_ID"]:
                    row1["ROAD_LENGTH_M"] = length

    osm_id_list.clear()

    for row in FINAL:
        if row["OSM_ID"] not in osm_id_list:
            osm_id_list.append(row["OSM_ID"])
            road_data = osm_data.get(row["OSM_ID"], None)
            highway = (
                road_data.get("highway", "unknown")
                if road_data is not None
                else "secondary"
            )
            for row1 in FINAL:
                if row1["OSM_ID"] == row["OSM_ID"]:
                    row1["KMH"] = MAXSPEED[highway]
                    row1["CATEGORY"] = highway.upper()

    with open("firstnormaldata20231108_logistic.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FINAL[0].keys())
        writer.writeheader()
        for row in FINAL:
            if row["ROAD_LENGTH_M"] != "unknown":
                writer.writerow(row)


JsonToCSV()
