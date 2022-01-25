import uuid
import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, DateTimeField, DynamicField, EmbeddedDocumentField, \
    EmbeddedDocumentListField, FloatField, IntField, ListField, LongField, ReferenceField, StringField, EmailField, \
    GenericReferenceField, DictField
from mongoengine.queryset.base import PULL

'''Embedded Doc for Agency and UserModel'''


class Address(EmbeddedDocument):
    street = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    pincode = LongField(required=True)


'''bus_stops_table'''


class BusStops(Document):
    name = StringField(Required=True)
    # meta = {
    #     'indexes':['name']
    # }


'''Embedded doc for bus_table'''


class Stops_Arrivals_Fare(EmbeddedDocument):
    # nor reverse so if bus deleted this will do nothing
    stops = ReferenceField(BusStops, required=True)
    # format is H:M h can be more than 24
    arrival_duration = StringField(required=True)
    fare_from_source = FloatField(required=True)


'''bus_table'''


class BusDetailsModel(Document):
    id = StringField(default=lambda: str(uuid.uuid4().hex), primary_key=True)
    bus_number = StringField(required=True)
    bus_name = StringField(required=True)
    base_fare = FloatField(required=True)
    # time of departure from source bus stop
    # HHMM
    departure_time = StringField(required=True)
    # List of (Embedded doc: each stops and the duration of time it takes to travel from source)
    stops_arrivals = EmbeddedDocumentListField(Stops_Arrivals_Fare)
    # stops_arrivals = DictField(field=)
    # fixed amount of seats provided to online from agency for this bus
    total_seats = IntField(Required=True)
    # Schedule of this bus repetition in TODO section
    schedule = DynamicField()
    # agency = GenericReferenceField(required=True,reverse_delete_rule=CASCADE)
    agency = GenericReferenceField()  # AgencyDetailModel
    # agency_id=StringField()

    # meta = {
    #     'db_alias': db_configurations.bus_details['alias'],
    #     'collection': db_configurations.bus_details['collection_name']
    # }


'''Embeddded Doc for tickets_table'''


class Passenger(EmbeddedDocument):
    name = StringField(required=True)
    age = IntField(required=True)
    gender = StringField(required=True)


'''tickets_table'''


class Tickets(Document):
    # _id = StringField(default=uuid.uuid4().hex)
    user = GenericReferenceField()
    # user_id=StringField(required=True)
    contact_number = StringField(required=True)
    bus = ReferenceField(BusDetailsModel, required=True)
    booking_date = DateTimeField(required=True)
    source = ReferenceField(BusStops, required=True)
    destination = ReferenceField(BusStops)
    # date of journey not required as we are can store date itself in departure and arrival
    departure_time = DateTimeField(required=True)
    arrival_time = DateTimeField(required=True)
    total_fare = FloatField(required=True)
    passenger_details = EmbeddedDocumentListField(Passenger)

    # payment_id = StringField(required=True)
    # meta = {
    #     'db_alias': db_configurations.user_ticket_details['alias'],
    #     'collection': db_configurations.user_ticket_details['collection_name']
    # }


'''User details Table'''


class UserDetailsModel(Document):
    id = StringField(default=lambda: str(uuid.uuid4().hex), primary_key=True)
    first_name = StringField(required=True)
    last_name = StringField()
    email = EmailField(required=True, unique=True)
    phone_number = StringField(required=True)
    hashed_password = StringField(required=True)
    # is_active = BooleanField(default=False)
    is_email_verified = BooleanField(default=False)
    account_type = StringField(default="user")
    address = EmbeddedDocumentField(Address)
    tickets = ListField(ReferenceField(Tickets, reverse_delete_rule=PULL))
    created_date = DateTimeField(default=datetime.datetime.now())
    deleted_date = DateTimeField(default=None)

    # meta = {
    #     'db_alias': db_configurations.user_info_details['alias'],
    #     'collection': db_configurations.user_info_details['collection_name']
    # }


'''agency_table'''


class AgencyDetailsModel(Document):
    id = StringField(default=lambda: str(uuid.uuid4().hex), primary_key=True)
    name = StringField(required=True)
    contact_number = StringField(required=True)
    email = EmailField()
    # bank details can be anything to be decide later for now dynamic data
    bank_details = DynamicField()
    agency_bus_list = ListField(ReferenceField(BusDetailsModel, reverse_delete_rule=PULL))
    agency_admin_list = ListField(ReferenceField(UserDetailsModel, reverse_delete_rule=PULL))
    address = EmbeddedDocumentField(Address)

    # meta = {
    #     'db_alias': db_configurations.agency_details['alias'],
    #     'collection': db_configurations.agency_details['collection_name']
    # }


'''Embedded Doc for date_bus_seat_table'''


class Bus_Seat(EmbeddedDocument):
    # nor reverse so if bus deleted this will do nothing
    # bus = ReferenceField(BusDetailsModel, required=True)
    # storing only id for better results while AVL seats query
    bus_id = StringField()
    seats = ListField(IntField())


'''for query 
(date) -> [bus & seats]

date_bus_seat_table'''


class Date_Bus_Seat_Model(Document):
    # date of journey
    # YYYYMMDD
    date = StringField(required=True, primary_key=True)
    # List of (embedded doc: Bus refs and seats for that day)
    bus_seats = EmbeddedDocumentListField(Bus_Seat)

    # meta = {
    #     'db_alias': db_configurations.bus_journey_details['alias'],
    #     'collection': db_configurations.bus_journey_details['collection_name']
    # }


'''for query 
(source, destination) -> [bus]

Source_Destination_Bus_table'''


class Source_Destination_Bus_Model(Document):
    source = StringField(Required=True)
    destination = StringField(Required=True)
    buses = ListField(ReferenceField(BusDetailsModel, reverse_delete_rule=PULL))
    # meta={
    #     'indexes':['source','destination']
    # }
