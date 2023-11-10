import json
from utils.road_length import road_length

list_of_ways = {}
list_of_nodes = {}

with open("newjsonfiles/osm.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for element in data["elements"]:
    if element["type"] == "node":
        list_of_nodes.update({element["id"]: (element["lat"], element["lon"])})

for element in data["elements"]:
    if element["type"] == "way":
        node_cords = []
        for node in element["nodes"]:
            node_cords.append(list_of_nodes[node])

        list_of_ways.update(
            {
                element["id"]: {
                    "highway": element["tags"].get("highway", "unknown"),
                    "length": round(road_length(node_cords)),
                    "max": element["tags"].get("maxspeed", "unknown"),
                }
            }
        )

with open("newjsonfiles/filtered_osm.json", "w") as f:
    json.dump(list_of_ways, f)
