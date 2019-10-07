#!/usr/bin/env python3
import flask
import subprocess
import random
import string
import os
import datetime
import pytz
from flask import Flask, request, render_template, redirect, jsonify

app = Flask(__name__)


# amixer  sset PCM,0 95%

textLimit = 200
nameLimit = 50
apiKey = os.getenv('API_KEY', '5u93r53cr37491k3y')

# The actual decorator function
def require_appkey(view_function):
  @wraps(view_function)
  # the new, post-decoration function. Note *args and **kwargs here.
  def decorated_function(*args, **kwargs):
    if 'api_key' in request.args and str(request.args['api_key']) == str(apiKey):
      return view_function(*args, **kwargs)
    else:
      abort(401)
    return decorated_function

@app.route('/')
def form():
  return render_template('form.html')

@app.route('/post', methods=['GET', 'POST'])
def poster():
  text = request.args.get('text').replace('\\', '').replace('\'', '').replace('\"', '')
  name = request.args.get('name')
  #text = request.form['text'].replace('\\', '').replace('\'', '').replace('\"', '')
  if not text:
    return redirect(request.url_root)
  #name = request.form['name']
  print(f'{request.remote_addr}|{name}> {text}')
  logger(text, name, request.remote_addr)
  illegal = []
  if any(bad in text for bad in illegal):
    return f'<h1 style="font-family: sans-serif;">Wait that\'s illegal! ({", ".join(illegal)})</h1>'
  if len(text) > textLimit or len(name) > nameLimit:
    return f'<h1>Message cannot exceed {limit} characters.</h1>'
  #subprocess.run(['say', f'{text}{". From " + name if name else ""}'])
  #subprocess.run(['echo', f'{text}{". From " + name if name else ""}', '|', 'festival', '--tts'])

  ps = subprocess.Popen(('echo', f'{text}{". From " + name if name else ""}'), stdout=subprocess.PIPE)
  output = subprocess.check_output(('festival', '--tts'), stdin=ps.stdout)
  ps.wait()

  if request.method == 'GET':
    return redirect(request.url_root)
  else:
    return jsonify('thank you')

def logger(message: str, user: str ='', ip: str = ''):
  time = str(datetime.datetime.now(pytz.timezone('Europe/Oslo')).strftime('%d-%m-%y %H:%M:%S'))
  #time = str(datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
  with open('messages.log', 'a') as logfile:
    logfile.write(f'[{user}@{ip}] {time} - {message}\n')


if __name__ == '__main__':
  app.config['DEBUG'] = False
  app.run(host='0.0.0.0', port=8009)

