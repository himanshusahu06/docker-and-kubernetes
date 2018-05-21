from flask import Flask

app = Flask(__name__)

@app.route("/")
def run():
    return "Hi There.."

@app.route("/hello")
def hello():
    return "Google.com"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
