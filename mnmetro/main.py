import json
import pprint

import requests


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

base_url = f"http://svc.metrotransit.org/NexTrip/"

pp = pprint.PrettyPrinter(indent=4)


class GetProviders(object):
    def __init__(self):
        self.name = "Providers"

    def info(self):
        r = requests.get(url=f"{base_url}{self.name}", headers=headers)
        return r.text

    # add one where it returns a list of all routes by provider


class GetRoutes(object):
    def __init__(self):
        self.name = "Routes"
        self.r = requests.get(url=f"{base_url}{self.name}", headers=headers).json() # I don't know if I want to call this in every instance under or keep it here, for here it will stay until I figure that out

    def all_routes(self):
        return pp.pprint(self.r)

    def route_ids(self):
        data = self.r.json()
        route_ids = []

        for route in data:
            route_ids.append(route["Route"])

        return pp.pprint(route_ids)

    def route(self, route_id):
        if not hasattr(route_id, "__pow__"):
            raise TypeError(f"{type(route_id)} is an unsupported operand. Should be an int.")

        for item in self.all_routes():
            if int(item["Route"]) == route_id:
                return item
        return f"The provided route_id: {route_id} does not appear in the Routes."


class GetDirections(object):
    """
    From the API docs: Returns the two directions that are valid for a given route. Either North/South or East/West. The result includes text/value pair with the direction name and an ID. Directions are identified with an ID value. 1 = South, 2 = East, 3 = West, 4 = North.

    """

    def __init__(self):
        self.name = "Directions"
    
    def direction_of(self, route_id):
        if not hasattr(route_id, "__pow__"):
            raise TypeError(f"{type(route_id)} is an unsupported operand. Should be an int.")

        self.route_id = int(route_id)

        return pp.pprint(requests.get(url=f"{base_url}{self.name}/{self.route_id}", headers=headers).json())


class GetStops(object):
    """
    From the API docs: Returns a list of Timepoint stops for the given Route/Direction. The result includes text/value pairs with the stop description and a 4 character stop (or node) identifier.

    # Adjust to be able to pass a list of route_ids and or directions
    """
    def __init__(self):
        self.name = "Stops"

    def stops_for(self, route_id, direction):
        """
        Maybe look into, if direction returns empty array showing available options for direction

        # I think we should adjust this to use directions as strings instead of ints
        """
        self.route_id = route_id
        self.direction = direction

        data = requests.get(url=f"{base_url}{self.name}/{self.route_id}/{self.direction}", headers=headers).json()

        if len(data) == 0:
            raise Exception(f"Looks to be an incorrect direction({self.direction}) or route_id({self.route_id})")
        else:
            return pp.pprint(data)


class GetDepartures(object):
    """
    From the API docs: This operation is used to return a list of departures scheduled for any given bus stop. A StopID is an integer value identifying any one of the many thousands of bus stops in the metro. Stop information can be derived from the GTFS schedule data updated weekly for public use. https://gisdata.mn.gov/dataset/us-mn-state-metc-trans-transit-schedule-google-fd
    """

    def __init__(self):
        pass

    def departure_for(self, stop_id):
        self.stop_id = stop_id

        data = requests.get(url=f"{base_url}{self.stop_id}", headers=headers).json()

        if len(data) == 0:
            raise Exception(f"Looks to be an incorrect direction({self.direction}) or route_id({self.route_id})")
        else:
            return pp.pprint(data)


class GetTimepointDepartures(object):
    """
    From the API docs: Returns the scheduled departures for a selected route, direction and timepoint stop.
    """

    def __init__(self):
        pass

    def times_for(self, route_id, direction, stop_id):
        self.route_id = route_id
        self.direction = direction
        self.stop_id = stop_id

        data = requests.get(url=f"{base_url}{self.route_id}/{self.direction}/{self.stop_id}", headers=headers).json()

        if len(data) == 0:
            raise Exception(f"Looks to be an incorrect direction({self.direction}) or route_id({self.route_id}) and or stop_id({self.stop_id})")
        else:
            return pp.pprint(data)


class GetVehicleLocations(object):
    """
    From the API docs: This operation returns a list of vehicles currently in service that have recently (within 5 minutes) reported their locations. A route paramter is used to return results for the given route. Use "0" for the route parameter to return a list of all vehicles in service.
    """

    def __init__(self):
        self.name = "VehicleLocations"
        self.route_id = 0

    def all_vehicles(self):
        return pp.pprint(requests.get(url=f"{base_url}{self.name}/{self.route_id}", headers=headers).json())

    def location_for(self, route_id):
        self.route_id = route_id
        return pp.pprint(requests.get(url=f"{base_url}{self.name}/{self.route_id}", headers=headers).json())