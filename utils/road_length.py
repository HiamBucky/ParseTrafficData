from geopy import distance


def road_length(road):
    return sum(distance.distance(road[i], road[i + 1]).m for i in range(len(road) - 1))
