from flask import Flask

app = Flask(__name__)

hit_count = 0

@app.route("/")
def root():
    return "Root\n"

@app.route("/counter")
def hello():
    global hit_count
    hit_count = hit_count + 1
    return "Hello World: " + str(hit_count) + " times\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7890)