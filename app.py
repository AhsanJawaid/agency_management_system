from flask  import Flask, render_template, request, redirect, url_for

from datetime import datetime
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path="/path/to/your/.env")

app = Flask(__name__)

@app.route('/', methods=["GET"])
def page_index():
    
    content = """
    <h1>Hello World!</h1>
    """
    
    return render_template("index.html", main_content=content)


if __name__ == "__main__":  
    
    app.run(host="localhost", port=os.getenv("APP_PORT", 0))
