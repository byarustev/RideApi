from pprint import pprint
from api.database.database_handler import DataBaseConnection


class Request:
    def __init__(self, ride, **kwargs):

        # all those keys will be initialized as class attributes
        allowed_keys = set(['request_id', 'requestor_id', 'owner_name', 'requestor_name', 'status'])

        # initialize all allowed keys to false
        self.__dict__.update((key, None) for key in allowed_keys)
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)

        self.ride_id = ride.ride_id
        self.origin = ride.origin
        self.destination = ride.destination
        self.departure_time = ride.departure_time
        self.slots = ride.slots
        self.description = ride.description
        self.owner_id = ride.user_id


class Ride:

    def __init__(self, **kwargs):

        # all those keys will be initialized as class attributes
        allowed_keys = set(['ride_id', 'user_id', 'origin', 'destination', 'departure_time', 'slots', 'description'])

        # initialize all allowed keys to false
        self.__dict__.update((key, None) for key in allowed_keys)
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)

    def create_ride(self):
        query_string = """
                      INSERT INTO rides (user_id, origin, destination, departure_time, slots, description) 
                      VALUES (%s,%s,%s,%s,%s,%s) RETURNING ride_id;
                      """
        try:
            connection = DataBaseConnection()
            cursor = connection.cursor
            cursor.execute(query_string, (self.user_id, self.origin, self.destination,
                                          self.departure_time, self.slots, self.description))

            return cursor.fetchone()[0]

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def create_ride_instance(row):
        temp_ride = Ride(ride_id=row["ride_id"], user_id=row["user_id"], origin=row["origin"], destination=row["destination"],
                         departure_time=row["departure_time"].strftime("%Y-%m-%d %H:%M:%S"), slots=row["slots"], description=row["description"])
        return temp_ride

    @staticmethod
    def create_request_instance(single_ride, row):
        temp_request = Request(single_ride, request_id=row["request_id"], requestor_id=row["requestor_id"],
                               owner_name=row["owner"], requestor_name=row["requestor"], status=row["status"])

        return temp_request

    @staticmethod
    def get_all_rides():
        query_string = """
                     SELECT * FROM rides
                     """
        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string)
            row = cursor.fetchone()

            db_rides = []

            while row:
                temp_ride = Ride.create_ride_instance(row)

                row = cursor.fetchone()
                db_rides.append(temp_ride.__dict__)

            return db_rides

        except Exception as exp:
            pprint(exp)
            return None

    def get_ride(self):
        query_string = "SELECT * FROM rides WHERE ride_id = %s "

        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string, (self.ride_id,))
            return cursor.fetchone()

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def create_ride_request(ride_id, user_id):
        query_string = "INSERT INTO ride_requests (ride_id,user_id,status) VALUES (%s,%s,%s) RETURNING request_id"
        try:
            connection = DataBaseConnection()
            cursor = connection.cursor
            cursor.execute(query_string, (ride_id, user_id, "pending"))
            return cursor.fetchone()[0]

        except Exception as exp:
            print(exp)
            return None

    @staticmethod
    def get_request(request_id):
        query_string = "SELECT * FROM ride_requests WHERE request_id = %s"

        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string, (request_id,))
            row = cursor.fetchone()
            return row

        except Exception as exp:
            pprint(exp)
            return "exp"

    @staticmethod
    def user_owns_ride(ride_id, user_id):
        query_string = "SELECT * FROM rides WHERE ride_id = %s AND user_id=%s"

        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string, (ride_id, user_id))
            row = cursor.fetchone()
            if row:
                return True
            else:
                return False

        except Exception as exp:
            pprint(exp)
            return False

    @staticmethod
    def update_ride_request(ride_id, request_id, status):
        query_string = """
                        UPDATE ride_requests SET status=%s
                        WHERE request_id=%s AND ride_id=%s
                     """
        try:
            connection = DataBaseConnection()
            cursor = connection.cursor
            cursor.execute(query_string, (status, request_id, ride_id))
            return True
        except Exception as exp:
            pprint(exp)
            return False

    @staticmethod
    def ride_requests(ride_id):
        query = """SELECT rq.request_id,rq.status,rq.user_id as requestor_id,rq.status,u.name as owner,u.user_id as owner_id,
                r.*,u2.name as requestor  FROM ride_requests rq
                LEFT JOIN rides r ON (r.ride_id=rq.ride_id)
                LEFT JOIN users u on (u.user_id=r.user_id)
                LEFT JOIN users u2 on (u2.user_id=rq.user_id)
                WHERE rq.ride_id=%s
                """
        try:
            connection = DataBaseConnection()
            dict_cursor = connection.dict_cursor
            dict_cursor.execute(query, (ride_id,))
            row = dict_cursor.fetchone()
            requests = []
            while row:
                ride = Ride.create_ride_instance(row)

                temp_request = Ride.create_request_instance(ride, row)

                requests.append(temp_request.__dict__)
                row = dict_cursor.fetchone()

            return requests

        except Exception as exp:
            pprint(exp)
