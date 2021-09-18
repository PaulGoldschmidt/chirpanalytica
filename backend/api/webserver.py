#! /usr/bin/env python3
from flask import Flask, request, jsonify, make_response, Response
from predict_account import predict_party
import time

app = Flask(__name__)

@app.route('/predict')
def predict():
    twitter_handle = request.args.get('user')
    r = make_response(jsonify(predict_party(twitter_handle))) # Raw output (including error, success and data field)
    r.headers.set('Access-Control-Allow-Origin', '*')
    return r

app.route('/progress') #testing progress bar
def progress():
	def generate():
		x = 0
		while x <= 100:
			yield "data:" + str(x) + "\n\n"
			x = x + 10
			time.sleep(0.5)
	return Response(generate(), mimetype= 'text/event-stream')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8879) #running locally behind reverse proxy
