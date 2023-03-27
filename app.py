import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/comments/")
def comments():
    youtube_api = os.getenv('YLYTIC_API')
    response = requests.get(youtube_api)
    return jsonify(response.json()), 200


if __name__ == '__main__':
    app.run(debug=True)
