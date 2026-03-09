import boto3

sns = boto3.client("sns", region_name="us-east-1")

TOPIC_ARN = "YOUR_TOPIC_ARN"


def send_booking_email(message):

    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:796973503140:TravelGo",
        Message=message,
        Subject="TravelGo Booking Confirmation"
    )
