from api.modals.ride import Ride
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class MyTrips(Resource):
    """MyTrips class inherits from Resource"""

    @jwt_required
    def get(self):
        """method get returns all the rides taken or offered by the logged in user"""

        user_id = get_jwt_identity()
        user_rides = Ride.my_offers(user_id)

        user_requests = Ride.my_requests(user_id)

        return {"status": "success", "message": "successful return",
                "my_rides": user_rides, "my_requests": user_requests}, 200
