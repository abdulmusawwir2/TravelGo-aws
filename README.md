
<img width="1620" height="478" alt="architecture" src="https://github.com/user-attachments/assets/b45262ed-c74b-402c-91a0-3f62f873358c" />

Youtube demo: https://youtu.be/apaxLLJ_Juw?si=UyRcjIKS1e6Z1HDi

COMMANDS:

# 1. Update system
sudo apt update

# 2. Install required packages
sudo apt install python3 -y
sudo apt install python3-venv -y
sudo apt install git -y

# 3. Clone your project
git clone https://github.com/abdulmusawwir2/TravelGo-aws.git

# 4. Go inside project folder
cd TravelGo-aws

# 5. Create virtual environment
python3 -m venv venv

# 6. Activate virtual environment
source venv/bin/activate

# 7. Install dependencies
pip install -r requirements.txt

# (Optional: if missing modules error comes)
pip install flask boto3

# run setup file to create db tables
python3 setup_aws.py

# 8. Run your app
python3 app.py


<img width="886" height="720" alt="image" src="https://github.com/user-attachments/assets/097c8509-f026-48e1-874e-b30c1087005d" />

# website live on : -<ec2ipaddress>:5000/login


# create and add role for ec2
dynamodbfull access
snsfull access

