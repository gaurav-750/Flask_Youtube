import os
import requests

from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def hello():
    return jsonify({"message": "Go to /comments/ or /comments/search/"}), 200


@app.route("/comments/")
def get_comments():
    youtube_api = os.getenv('YLYTIC_API')
    response = requests.get(youtube_api)
    return jsonify(response.json()), 200


def get_date(input_date):  # Sat, 1 Jan 2023 01:55:35 GMT
    input_format = "%a, %d %b %Y %H:%M:%S %Z"
    output_format = "%d-%m-%Y"
    date_obj = datetime.strptime(input_date, input_format)

    return date_obj.strftime(output_format)  # Output: 01-01-2023


# /search?search_author=Fredrick
@app.route("/comments/search/")
def get_filtered_comments():

    # *extracting the params from the url
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    youtube_api = os.getenv('YLYTIC_API')
    response = requests.get(youtube_api)
    # handling error
    if response.status_code != 200:
        return {"error": "Something went wrong"}, response.status_code

    # get all the comments
    filtered_comments = response.json()['comments']

    if search_author:
        filtered_comments = [
            comment for comment in filtered_comments if comment['author'].lower() == search_author.lower()]

    if at_from:
        filtered_comments = [
            comment for comment in filtered_comments if get_date(comment['at']) >= at_from]
    if at_to:
        filtered_comments = [
            comment for comment in filtered_comments if get_date(comment['at']) <= at_to]

    if like_from:
        filtered_comments = [
            comment for comment in filtered_comments if comment['like'] >= int(like_from)]
    if like_to:
        filtered_comments = [
            comment for comment in filtered_comments if comment['like'] <= int(like_to)]

    if reply_from:
        filtered_comments = [
            comment for comment in filtered_comments if comment['reply'] >= int(reply_from)]

    if reply_to:
        filtered_comments = [
            comment for comment in filtered_comments if comment['reply'] <= int(reply_to)]

    if search_text:
        filtered_comments = [
            comment for comment in filtered_comments if search_text.lower() in comment['text'].lower()]

    return {"comments": filtered_comments}, 200


if __name__ == '__main__':
    app.run(debug=True)
