import boto3

sns = boto3.client("sns", region_name="us-east-1")

TOPIC_ARN = "YOUR_TOPIC_ARN"


def send_booking_email(message):

    sns.publish(
        TopicArn="arn:aws:sns:ap-south-1:219817681192:TravelGo",
        Message=message,
        Subject="TravelGo Booking Confirmation"
    )
