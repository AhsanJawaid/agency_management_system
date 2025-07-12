from app import create_app
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Set the secret key from environment variable or use a default
SECRET_KEY = os.getenv('SECRET_KEY', '8f0629a3c5f177edd835dc9dde03fd9e6c25d5aa211ade1eaf46db1c6325d03f')


app = create_app()

if __name__ == '__main__':
    app.run(host="localhost", port=os.getenv('APP_PORT'),debug=True)