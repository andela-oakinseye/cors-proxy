import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
def hello_world():
  url = request.args.get('url')
  base = url
  head = {
    'Host': url,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92',
    }
  response = requests.get(base, allow_redirects=True)
  return jsonify(json.loads(response.content))

if __name__ == '__main__':
   app.run()