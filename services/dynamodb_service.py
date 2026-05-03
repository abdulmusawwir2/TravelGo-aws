import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

users_table = dynamodb.Table('Users')
bookings_table = dynamodb.Table('Bookings')


# Add User
def create_user(email, name, password):

    users_table.put_item(
        Item={
            'email': email,
            'name': name,
            'password': password,
            'logins': 0
        }
    )


# Get User
def get_user(email):

    response = users_table.get_item(
        Key={'email': email}
    )

    return response.get('Item')


# Create Booking
def create_booking(email, type, source, destination, date, seat, price):

    booking_id = str(uuid.uuid4())

    bookings_table.put_item(
        Item={
            "booking_id": booking_id,
            "email": email,
            "type": type,
            "source": source,
            "destination": destination,
            "date": date,
            "seat": seat,
            "price": price
        }
    )

    return booking_id
# Get bookings of a user
def get_user_bookings(email):

    response = bookings_table.scan(
        FilterExpression="email = :e",
        ExpressionAttributeValues={
            ":e": email
        }
    )

    return response.get("Items", [])
