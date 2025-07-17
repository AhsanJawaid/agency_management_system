from app import create_app, socketio
import os

application = create_app()

if __name__ == '__main__':
    socketio.run(application, host="localhost", port=os.getenv('APP_PORT'),debug=True)