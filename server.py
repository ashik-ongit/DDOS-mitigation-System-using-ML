from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Protected Website"

@app.route("/data")
def data():
    return "Sensitive Data"

if __name__ == "__main__":
    app.run(port=5000)
