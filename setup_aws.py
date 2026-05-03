import boto3
import time

# ======================
# CONFIG (EDIT THIS)
# ======================
REGION = "ap-south-1"
EMAIL = "abdul.musawwir276@gmail.com"   # 🔥 put your email here

# ======================
# CLIENTS
# ======================
dynamodb = boto3.client("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

# ======================
# CREATE USERS TABLE
# ======================
def create_users_table():
    try:
        dynamodb.describe_table(TableName="Users")
        print("Users table already exists ✅")
    except:
        dynamodb.create_table(
            TableName="Users",
            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print("Creating Users table...")
        wait_for_table("Users")


# ======================
# CREATE BOOKINGS TABLE
# ======================
def create_bookings_table():
    try:
        dynamodb.describe_table(TableName="Bookings")
        print("Bookings table already exists ✅")
    except:
        dynamodb.create_table(
            TableName="Bookings",
            KeySchema=[
                {"AttributeName": "booking_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "booking_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print("Creating Bookings table...")
        wait_for_table("Bookings")


# ======================
# WAIT FOR TABLE
# ======================
def wait_for_table(table_name):
    while True:
        response = dynamodb.describe_table(TableName=table_name)
        status = response["Table"]["TableStatus"]

        if status == "ACTIVE":
            print(f"{table_name} table ready ✅")
            break

        print(f"Waiting for {table_name}...")
        time.sleep(2)


# ======================
# CREATE SNS TOPIC
# ======================
def create_sns_topic():
    response = sns.create_topic(Name="TravelGo")
    topic_arn = response["TopicArn"]

    print("SNS Topic ARN:", topic_arn)

    # Save ARN locally
    with open("sns_arn.txt", "w") as f:
        f.write(topic_arn)

    return topic_arn


# ======================
# SUBSCRIBE EMAIL
# ======================
def subscribe_email(topic_arn):
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol="email",
        Endpoint=EMAIL
    )
    print("📧 Subscription request sent!")
    print("👉 Check your email and CONFIRM subscription")


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    print("🚀 Setting up AWS resources...\n")

    create_users_table()
    create_bookings_table()

    arn = create_sns_topic()
    subscribe_email(arn)

    print("\n✅ Setup Complete!")
    print("👉 SNS ARN saved in sns_arn.txt")
