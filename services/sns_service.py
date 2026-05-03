import boto3
import os
from dotenv import load_dotenv

load_dotenv()

sns = boto3.client("sns", region_name=os.getenv("AWS_REGION"))

TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

def send_booking_email(message):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject="TravelGo Booking Confirmation"
    )
