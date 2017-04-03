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
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'direct'
    }

  response = requests.get(base, headers=headers, allow_redirects=True, verify=False)
  error_response = {'message': 'Error fetching data, check request'}
  t = request.values.get('t', 0)
  time.sleep(float(t)) #just to show it works...
  if(response.status_code == 200 and 'application/json' in response.headers["Content-Type"]):
    print g.request_time()
    return jsonify(json.loads(response.content))
  else:
    return jsonify(error_response)

if __name__ == '__main__':
   app.run()