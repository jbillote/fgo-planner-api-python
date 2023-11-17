from flask import Flask

app = Flask(__name__)

@app.route("/api/fgo/v1/servant", methods=["GET"])
def servant_search():
    return { "message": "Hello world!" }
