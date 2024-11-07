import os
from dotenv import load_dotenv
load_dotenv()

isProd = os.environ.get("PROD")=="true"
apiUrl=os.environ["API_URL"]
apiKey=os.environ["API_KEY"]
secretName=os.environ["DFK_SECRET_NAME"]