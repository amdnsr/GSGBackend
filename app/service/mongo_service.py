from datetime import datetime, timedelta
from typing import List

from mongoengine.connection import connect, disconnect

from app.core.security import get_password_hash
from app.models.request_response_models import *
from app.service.schema_models_zia import *
from app.core.security import verify_password

class MongoService:
    @classmethod
    def make_connection(cls, mongo_connection_info):
        """To create connection to mongodb"""
        if mongo_connection_info.get('mongo_env') in ["STAGE", "PRODUCTION"]:
            connect(
                alias=mongo_connection_info.get('alias', 'default'),
                db=mongo_connection_info.get('db_name'),
                host=mongo_connection_info.get('host_name'),
                port=mongo_connection_info.get('host_port'),
                username=mongo_connection_info.get('username'),
                password=mongo_connection_info.get('password'),
            )
        else:
            connect(
                alias=mongo_connection_info.get('alias', 'default'),
                db=mongo_connection_info.get('db_name'),
                host=mongo_connection_info.get('host_name'),
                port=mongo_connection_info.get('host_port')
            )

    @classmethod
    def close_connection(cls, mongo_connection_info):
        """close connection from mongo db"""
        disconnect(alias=mongo_connection_info.get('alias'))

    """################# Api Bus Related Query Start #########################"""

    """Method to get All bus stop names from db
    @param NONE
    @return List of String Bus name
    """

    @classmethod
    def get_all_bus_stops(cls):
        """return the list of String : names of bus stops"""
        return [value.name for value in BusStops.objects.only()]

    """Populate Response body List of Bus Details Model from date source destination 
    @param BookingQueryRequest-> date, source, destination
    @return 
    """

    @classmethod
    def get_bus_list(cls, request: BookingQueryRequest, response: BookingQueryResponse):
        """return Booking Query response"""
        # src: BusStops = BusStops.objects(name=request.source).first()
        # dest: BusStops = BusStops.objects(name=request.destination).first()
        src: str = request.source
        dest: str = request.destination
        # date format should be YYYYMMDD
        dt: str = request.date_of_journey

        # step 1-> retrieve the list of {bus id,seats} objects which run on this date
        #           from date_bus_seat_table
        list_of_bus_seats: list[Bus_Seat] = Date_Bus_Seat_Model.objects(date=dt).first().bus_seats
        map_of_bus_id_seats = {item.bus_id: item.seats for item in list_of_bus_seats}

        # step 2-> retrieve the list of busses which travel from this source(bus stop) to destination(bus stop)
        #           from source_destination_bus_table
        list_of_bus: list[BusDetailsModel] = Source_Destination_Bus_Model.objects(source=src,
                                                                                  destination=dest).first().busses

        # step 3-> $(step1) retain all $(step2) : intersection
        # result = [value for value in list_of_bus_seats if value.bus in list_of_bus]
        result = []
        for tmp_bus in list_of_bus:
            if tmp_bus.id in map_of_bus_id_seats.keys():
                tup = (tmp_bus, map_of_bus_id_seats.get(tmp_bus.id))
                result.append(tup)

        # step 4-> populate response object from $(step3)
        response.result = []

        for each in result:
            # no need now to recheck the existence of bus
            #     try:
            #         bus: BusDetailsModel = each.bus
            #     except:
            #         continue

            bus: BusDetailsModel = each[0]

            singleBusResult = SingleBusResult()
            singleBusResult.id = bus.id
            singleBusResult.source = src
            singleBusResult.destination = dest
            singleBusResult.date_of_journey = dt
            singleBusResult.bus_name = bus.bus_name
            singleBusResult.bus_number = bus.bus_number
            singleBusResult.agency_name = bus.agency.name

            stop_name_list = [item.stop.name for item in bus.stops_arrivals]
            arrival_time_list = [item.arrival_duration for item in bus.stops_arrivals]

            # for dep and arrival times
            singleBusResult.departure_time = datetime.datetime.strptime(dt + ' ' + bus.departure_time, '%Y%I%d %H:%M')
            # departure time + duration = arrival Time
            # start = datetime.strptime(bus.departure_time, '%H:%M')
            singleBusResult.arrival_time = singleBusResult.departure_time + cls._get_travel_duration(stop_name_list,
                                                                                                     arrival_time_list,
                                                                                                     src,
                                                                                                     dest)
            # for fare
            fare_list = [item.fare_from_source for item in bus.stops_arrivals]
            singleBusResult.fare_for_one_seat = bus.base_fare + cls._get_fare(stop_name_list, fare_list, src, dest)

            # avl seats
            singleBusResult.no_of_seats_available = cls._get_seats_avl(stop_name_list,
                                                                       each[1], src, dest)  # each.seats

            response.result.append(singleBusResult)

    """Private method to get fare diffs from src to dest 
    @param list of stops str, list of float of fares correspondingly, src str, dest str
    @return int
    """

    @classmethod
    def _get_fare(cls, stops_list: List[str], fare_list: List[float], source: str,
                  destination: str):
        try:
            src: int = stops_list.index(source)
            dest: int = stops_list.index(destination)
        except:
            print("src or destination in not present for this bus")  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            return 0

        return fare_list[dest] - fare_list[src]

    """Private method to get travel duration from src to dest 
        @param list of stops str, list of time duration correspondingly, src str, dest str
        @return int
        """

    @classmethod
    def _get_travel_duration(cls, stops_list: List[str], arrivals_list: List[int], source: str,
                             destination: str):
        try:
            src: int = stops_list.index(source)
            dest: int = stops_list.index(destination)
        except:
            print("src or destination in not present for this bus")  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            return 0
        s = arrivals_list[dest]
        arr = s.split(':')
        days = int(arr[0]) % 24
        s = str(int(arr[0]) // 24) + ':' + arr[1]
        dep = datetime.datetime.strptime(s, '%H:%M')
        dep = dep + timedelta(days=days)

        s = arrivals_list[src]
        arr = s.split(':')
        days = int(arr[0]) % 24
        s = str(int(arr[0]) // 24) + ':' + arr[1]
        src = datetime.datetime.strptime(s, '%H:%M')
        src = src + timedelta(days=days)

        return dep - src

    """Private method to get seat AVl from src to dest 
    @param list of stops str, list of int seats correspondingly, src str, dest str
    @return int
    """

    @classmethod
    def _get_seats_avl(cls, stops_list: List[str], seats_list: List[int], source: str,
                       destination: str):
        """private helper method Return the current seats avl for given date"""
        seat = 1000000  # max value
        try:
            src: int = stops_list.index(source)
            dest: int = stops_list.index(destination)
        except:
            print("src or destination in not present for this bus")  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            return 0

        for i in range(src, dest + 1):
            seat = min(seats_list[i], seat)
        return seat

    """ Method to query Seats AVL now  simply populate response model
    @param CurrentSeatsAvlRequest -> Bus Id, date, Src, Dest
    @return  CurrentSeatsAvlResponse -> Int avl_seats
    """

    @classmethod
    def get_current_seats_avl(cls, request: CurrentSeatsAvlRequest, response: CurrentSeatsAvlResponse):
        """query response for current seats avl"""
        # ~select bus_seats(list of bus_seats) as lbs
        # ~from Date_Bus_Seat_Model
        # ~where date = req.dt
        # lbs[bus_id=req.bus_id].seats -> list[int] : seats_list
        lbs = Date_Bus_Seat_Model.objects(date=request.date).first().bus_seats  # .seats
        seats_list = next(item.seats for item in lbs if item.bus_id == request.bus_id)

        # retrieve bus from bus id and get list of stops
        stops_arrival_from_bus = BusDetailsModel.objects(id=request.bus_id).only(
            'stops_arrivals').first().stops_arrivals
        stops_list = [item.stops.name for item in stops_arrival_from_bus]

        # search from src to dest and pick min seats avl
        bus: BusDetailsModel = BusDetailsModel.objects(id=request.busId).first()
        seats_list: list[int] = Date_Bus_Seat_Model.objects(date=request.date,
                                                            bus_seats__bus=bus).first().bus_seats.seats

        response.avlSeats = cls._get_seats_avl(stops_list, seats_list, request.source, request.destination)
        return response

    @classmethod
    def get_ticket_by_id(cls, ticket_id: str):
        # TODO
        return

    @classmethod
    def add_bus_to_src_dest_bus_table(cls, bus: BusDetailsModel):
        # TODO
        return

    """~~~~~~~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """################### User Related ####################################"""

    """ ADD NEW USER to DB 
    @param CreateAccountRequest request
    @return Created User 
    """

    @classmethod
    def add_new_user(cls, request: CreateAccountRequest):
        newUser = UserDetailsModel()

        # assuming the password and confirm_password match
        newUser.first_name = request.first_name
        newUser.last_name = request.last_name
        newUser.email = request.email
        newUser.hashed_password = get_password_hash(request.password)
        if request.phone_number is not None:
            newUser.phone_number = request.phone_number

        return newUser.save()

    """ Check if a user exists with this email 
    @param string email
    @return Boolean/User
    """

    @classmethod
    def get_user_details_by_email(cls, email: str):
        user = UserDetailsModel.objects(email=email).first()
        if not user:
            return False
        user = UserProfileResponse.parse_obj(user.to_mongo().to_dict())
        return user

    """ Verify User Email After SignUp 
    @param string email
    @return Boolean
    """

    @classmethod
    def verify_user_email(cls, email: str):
        myUser: UserDetailsModel = UserDetailsModel.objects(email=email).first()
        if myUser is None:
            return False
        myUser.update(set__is_email_verified=True)
        return True

    """ User Login Validation Request -> User Credentials Are Correct or not
    @param LoginRequest request
    @return Boolean
    """

    @classmethod
    def validate_user_login(cls, request: LoginRequest):
        myUser: UserDetailsModel = UserDetailsModel.objects(email=request.email).first()
        if myUser is None:
            return False
        if verify_password(request.password, myUser.hashed_password):
            return True
        return False

    """ Reset Password request 
    @param email, new_password
    @return Boolean Success Status
    """

    @classmethod
    def reset_user_password(cls, email, new_password):
        # assuming the new_password and confirm_new_password match
        myUser: UserDetailsModel = UserDetailsModel.objects(email=email).first()
        if myUser is None:
            return False
        new_hashed_password = get_password_hash(new_password)
        myUser.update(set__hashed_password=new_hashed_password)
        return True

    """ Update Password request 
    @param email, old_password, new_password
    @return Boolean Success Status
    """

    @classmethod
    def update_user_password(cls, email, old_password, new_password):
        # assuming the new_password and confirm_new_password match
        myUser: UserDetailsModel = UserDetailsModel.objects(email=email).first()
        if myUser is None:
            return False
        if not verify_password(old_password, myUser.hashed_password):
            return False
        new_hashed_password = get_password_hash(new_password)
        myUser.update(set__hashed_password=new_hashed_password)
        return True

    """ Delete User by Email Address
    @param String Email
    @return Boolean Success Status
    """

    @classmethod
    def delete_user(cls, email: str):
        myUser: UserDetailsModel = UserDetailsModel.objects(email=email).first()
        if myUser is None:
            return False
        myUser.delete()
        return True

    # #TODO add get_user_details_by_email function
    
    """~~~~~~~~~~~~~~~~~~~~ END USER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """################# AGENCY Related ####################################"""

    """Private Method to populate bus attributes from request model
    @param BusDetailsModel new_bus, EachBusFromAgency each_bus
    @return 
    """

    @classmethod
    def _populate_new_bus(cls, new_bus: BusDetailsModel, each_bus: EachBusFromAgency):
        new_bus.bus_name = each_bus.bus_name
        new_bus.bus_number = each_bus.bus_number
        new_bus.base_fare = each_bus.base_fare
        new_bus.departure_time = each_bus.departure_time
        new_bus.stops_arrivals = []
        for i in range(len(each_bus.list_of_stops)):
            stop_arrival_obj = Stops_Arrivals_Fare()

            stop_name = each_bus.list_of_stops[i]
            stop: BusStops = BusStops.objects(name=stop_name).first()
            if stop is None:
                stop = BusStops()
                stop.name = stop_name
                stop.save()

            stop_arrival_obj.stops = stop
            stop_arrival_obj.arrival_duration = each_bus.list_of_arrival_duration_from_src[i]
            stop_arrival_obj.fare_from_source = each_bus.list_of_fare_from_source[i]

            new_bus.stops_arrivals.append(stop_arrival_obj)

        new_bus.total_seats = each_bus.total_seat
        new_bus.schedule = each_bus.schedule
        return

    """Method to ADD NEW AGENCY DETAILS to DB 
    @param AddAgencyDetailsRequest request
    @return
    """

    @classmethod
    def Add_agency_details(cls, request: AddAgencyDetailsRequest):
        new_agency = AgencyDetailsModel()

        new_agency.name = request.agency_name
        new_agency.contact_number = request.agency_contact_number
        new_agency.email = request.agency_email
        new_agency.bank_details = request.agency_bank_details
        address = Address()
        address.street = request.agency_address_street
        address.city = request.agency_address_city
        address.state = request.agency_address_state
        address.pincode = request.agency_address_pincode
        new_agency.address = address
        new_agency.agency_bus_list = []
        for i in range(len(request.list_of_bus)):
            new_bus = BusDetailsModel()
            cls._populate_new_bus(new_bus, request.list_of_bus[i])
            new_bus.agency = new_agency
            new_bus.save()
            new_agency.agency_bus_list.append(new_bus)

        new_agency.save()
        return True

    """ Method to UPDATE bus attributes from request model bu AGENCY
    @param UpdateBusDetailRequest request
    @return 
    """

    @classmethod
    def update_bus_detail(cls, request: UpdateBusDetailRequest):
        bus = BusDetailsModel.objects(id=request.bus_id).first()
        if bus is None:
            return False
        cls._populate_new_bus(bus, UpdateBusDetailRequest)
        bus.save()
        return True

    """ Method to DELETE Bus Request by AGENCY 
    @param DeleteBusDetailRequest request
    @return
    """

    @classmethod
    def delete_bus_detail(cls, request: DeleteBusDetailRequest):
        bus = BusDetailsModel.objects(id=request.bus_id).first()
        if bus is None:
            return False
        bus.delete()
        return True

    """~~~~~~~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
