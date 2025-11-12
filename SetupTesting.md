Use VSC to create virtual environment, it would ask for requirement.txt file
export PYTHONPATH=$PYTHONPATH:/Users/yogeshkumar/customer-support-agent/backend

below setting worked for interactive compiling 
Add this at the very top of your vectordb.py file (above your imports):
import sys, os

# get the current file directory (this file = backend/app/database/vectordb.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# go up 2 levels to reach backend/
backend_dir = os.path.abspath(os.path.join(current_dir, "../.."))

# ensure backend is in sys.path so we can import 'app'
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# now this should work
from app.config.settings import get_settings

How to Kill the application 

lsof -i :8000
kill -9 8421

How to Start
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

Running docker container (changes from default files)
Would need .env file in same directory

Git Versioning
1) .gitingore for ingnoring the files which we dont want to commit
    push it to github

#Deployment steps on AWS ECR - ECS Fargate

0.1) Authenticlate to ECR
1) Creage docker image on local machine.
2) Create ECR on AWS - Ideally use IAM user.
    verify if the build is compatiable with ECS Fargate
        docker image inspect f17944c6b0cd --format='{{.Os}}/{{.Architecture}}'
3) Register/Push docker image from local machine to AWS ECR using AWS CLI 
4) Secret Manager
    create secret and use arn in value from while creating the task
5) Create Task definetion in ECS.
    add environment vars from .env file except openai_api_key should point to aws secret manager
    allowed_origins - keep it as * for now, later replace by ALB url
    Alternatively I oculd have used .env kind of file to upload (except API key)
    Health check need to be setup as we have exposed /health endpoint
    Choice of storage EBS or inside default Fargate
6) Create Cluser under ECS    
    failed with permission error    
    re-atempted and it worked fine this time.
7) Create Container service under cluster
    Compute Conf
        select Launch Type
        tick availability zone re-balancing
    Deployment Options
        Chose rolling update
    Networking
        keep default vpc
        keep 2 subnets in different regions
        'Create new security group'
        Inbound
            Type - HTTP, Source 0.0.0.0/0
    Load balancing
        tick
        listner
            create new
        Target Group
            create new
            health check path - /health
    Service auto scaling
        Unticked

    Create Service
        failed with error
            looks like ecsextcutetask does not have permittion to secret keys

    Task run failed because of image mismatch
        rebuild image with multi build

    Task run failed
        looks like because of open api key issue
        Fix - converted api key format from json to plaintext
    Task run failed again
        Looks like memory issue  
        not memory issue  

    appilcation is designed to run on port 8000
    ALB was on port 80 - changed to 8000
    Security group has inbound trafic for port 80
        added one more in bound rule for 8000

Complete Configuration Check:
After adding the rule, your setup should be:
ALB Listener: Port 8000 ✅
Target Group: Port 8000 ✅
Security Group: Allows port 8000 ✅
Container: Running on port 8000 ✅