from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend root OK", 200

@app.route("/test")
def test():
    return "Backend test OK", 200

if __name__ == "__main__":
    print("Backend running on port 5000")
    app.run(port=5000)
