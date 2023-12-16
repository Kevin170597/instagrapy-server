from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI=os.environ.get('MONGODB_URI')
BULLWORTHPICS_PASSWORD=os.environ.get('BULLWORTHPICS_PASSWORD')

JWT_SECRET_ENCODER=os.environ.get('JWT_SECRET_ENCODER')
JWT_ALGORITHM=os.environ.get('JWT_ALGORITHM')
