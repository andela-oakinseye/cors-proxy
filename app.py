import time
import requests
import requests_cache
import json
from flask import Flask, request, jsonify, g

# Cache requests into a DB to avoid calling over and over
requests_cache.install_cache('cached_data')

app = Flask(__name__)

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
def fetch_json():
  url = request.args.get('url')
  base = url
  head = {
    'Host': url,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92',
    }
  response = requests.get(base, allow_redirects=True)
  error_response = {'message': 'Error connecting to destination \n ensure it is a valid json'}
  t = request.values.get('t', 0)
  time.sleep(float(t)) #just to show it works...
  if(response.status_code == 200 and 'application/json' in response.headers["Content-Type"]):
    print g.request_time()
    return jsonify(json.loads(response.content))
  else:
    return jsonify(error_response)

if __name__ == '__main__':
   app.run()