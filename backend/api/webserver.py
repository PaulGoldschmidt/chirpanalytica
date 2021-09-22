#! /usr/bin/env python3
from flask import Flask, request, jsonify, make_response
from predict_account import predict_party

app = Flask(__name__)


@app.route('/predict')
def predict():
    twitter_handle = request.args.get('user')
    # Raw output (including error, success and data field)
    r = make_response(jsonify(predict_party(twitter_handle)))
    r.headers.set('Access-Control-Allow-Origin', '*')
    return r


if __name__ == '__main__':
    # Running locally behind reverse proxy
    app.run(host="127.0.0.1", port=8879)
