# import uuid

# from mongoengine import BooleanField, Document, DictField, DateField, DateTimeField, FloatField, IntField, ListField, StringField

# from app.config.configurations import DBConfig

# db_configurations = DBConfig()


# class BusJourneyDetailsModel(Document):
#     date_of_journey = DateField(required=True)
#     bus_ids = ListField(required=True)  # references BusModelInsert's bus_id
#     meta = {'db_alias': db_configurations.bus_journey_details['alias'],
#             'collection': db_configurations.bus_journey_details['collection_name']}


# class BusDetailsModel(Document):
#     bus_id = StringField(default=uuid.uuid4().hex)
#     bus_number = StringField(required=True)
#     bus_name = StringField(required=True)
#     agency_id = StringField(required=True)
#     source = str
#     destination = str
#     list_of_stops = ListField(required=True)
#     departure_time = DateTimeField(required=True)  # from the first station
#     arrival_time = DateTimeField(required=True)  # at the last station
#     # DateTimeField values for each intermediate station
#     list_of_arrival_times = ListField(required=True)
#     base_fair = FloatField(required=True)
#     # FloatField values for each intermediate station
#     list_of_fairs_from_origin = ListField(required=True)
#     meta = {'db_alias': db_configurations.bus_details['alias'],
#             'collection': db_configurations.bus_details['collection_name']}


# class AgencyDetailsModel(Document):
#     agency_id = StringField(default=uuid.uuid4().hex)
#     agency_name = StringField(required=True)
#     address = StringField(required=True)
#     contact_number = StringField(required=True)
#     bank_details = StringField(required=True)
#     agency_bus_list = ListField()  # list of bus_id from BusDetailsModel
#     agency_admin_list = ListField()  # list of user_id from AgencyUserModel
#     meta = {'db_alias': db_configurations.agency_details['alias'],
#             'collection': db_configurations.agency_details['collection_name']}


# class AgencyUserDetailsModel(Document):
#     agency_user_id = StringField(default=uuid.uuid4().hex)
#     email = StringField(required=True)
#     hashed_password = StringField(required=True)
#     meta = {'db_alias': db_configurations.agency_user_details['alias'],
#             'collection': db_configurations.agency_user_details['collection_name']}


# class JourneySeatDetailsModel(Document):
#     bus_id = StringField(required=True)
#     date_of_journey = DateField(required=True)
#     no_of_seats_available = IntField(required=True)
#     meta = {'db_alias': db_configurations.journey_seat_details['alias'],
#             'collection': db_configurations.journey_seat_details['collection_name']}


# class UserInfoDetailsModel(Document):
#     user_id = StringField(default=uuid.uuid4().hex)
#     first_name = StringField(required=True)
#     last_name = StringField(required=True)
#     email = StringField(required=True)
#     phone_number = StringField(required=True)
#     hashed_password = StringField(required=True)
#     is_active = BooleanField(default=False)
#     account_type = StringField(default="user")
#     meta = {'db_alias': db_configurations.user_info_details['alias'],
#             'collection': db_configurations.user_info_details['collection_name']}


# class PassengerDetailsModel(Document):
#     passenger_name = StringField(required=True)
#     passgenger_age = IntField(required=True)
#     passenger_gender = StringField(required=True)


# class UserTicketDetailsModel(Document):
#     ticket_id = StringField(default=uuid.uuid4().hex)
#     user_id = StringField(required=True)
#     source = StringField(required=True)
#     destination = StringField(required=True)
#     date_of_journey = DateField(required=True)
#     departure_time = DateTimeField(required=True)
#     passenger_details = ListField()  # list of PassengerDetailsModel
#     contact_number = StringField(required=True)
#     total_payment_amount = FloatField(required=True)
#     payment_id = StringField(required=True)
#     meta = {'db_alias': db_configurations.user_ticket_details['alias'],
#             'collection': db_configurations.user_ticket_details['collection_name']}


# class TicketPaymentDetails(Document):
#     payment_id = StringField(default=uuid.uuid4().hex)
#     total_payment_amount = FloatField(required=True)
#     payment_details = Document()  # details from payment provider
