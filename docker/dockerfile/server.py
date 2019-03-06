from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def run():
    return "Hi There..\n"

@app.route("/hello")
def hello():
    return "Google.com\n"

if __name__ == "__main__":
    server_port = os.getenv('PYTHON_SERVER_PORT', None)
    if server_port is None:
        raise ValueError("server port not found. Please set PYTHON_SERVER_PORT env variable.")
    app.run(host='0.0.0.0', port=int(server_port))
