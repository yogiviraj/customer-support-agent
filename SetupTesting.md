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
