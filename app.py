#!/usr/bin/env python3
import flask
import subprocess
import random
import string
import os
import sys
import datetime
import pytz
import logging
from flask import Flask, request, render_template, redirect, jsonify

app = Flask(__name__)


# amixer  sset PCM,0 95%

text_limit = 200
name_limit = 50
api_key = os.getenv('API_KEY', '5u93r53cr37491k3y')
port = os.getenv('PORT', 8009)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s', # %(name)s
    datefmt='%d/%m/%Y %H:%M:%S'
)
log = logging.getLogger(__name__)

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if 'api_key' in request.args and str(request.args['api_key']) == str(api_key):
            return view_function(*args, **kwargs)
        else:
            abort(401)
        return decorated_function

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/post', methods=['GET', 'POST'])
def poster():
    name = request.args.get('name')
    text = request.args.get('text') \
        .replace('\\', 'backslash') \
        .replace('\'', 'quote') \
        .replace('\"', 'quotes') \
        .replace('|', 'pipe') \
        .replace(';', 'semicolon') \
        .replace('&', 'and') \
        .replace('<', 'less than') \
        .replace('>', 'greater than') \
        .replace('$', 'dollar') \
        .replace('`', 'tick')
    #name = request.form['name']
    #text = request.form['text'].replace('\\', '').replace('\'', '').replace('\"', '')
    if not text:
        return redirect(request.url_root)
    log.info(f'{name}@{request.remote_addr} {text}')
    illegal = []
    if any(bad in text for bad in illegal):
        return f'<h1 style="font-family: sans-serif;">Wait that\'s illegal! ({", ".join(illegal)})</h1>'
    if len(text) > text_limit or len(name) > name_limit:
        return f'<h1 style="font-family: sans-serif;">' \
               f'Message cannot exceed {text_limit} characters.<br/>' \
               f'Name cannot exceed {name_limit} characters.</h1>'

    ps = subprocess.Popen(('echo', f'{text}{". From " + name if name else ""}'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('festival', '--tts'), stdin=ps.stdout)
    ps.wait()

    if request.method == 'GET':
        return redirect(request.url_root)
    else:
        return jsonify('thank you for the kind words')

if __name__ == '__main__':
  app.config['DEBUG'] = True
  app.run(host='0.0.0.0', port=port)
