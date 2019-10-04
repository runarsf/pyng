#!/usr/bin/env python3
import flask
import subprocess
import random
import string
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


limit: int = 300

@app.route('/')
def form():
  return render_template('form.html')

# Save to file using gTTS (slow)
#@app.route('/', methods=['POST'])
#def poster():
#  text = request.form['text']
#  language = 'en'
#  filename = f'{"".join(random.choice(string.ascii_lowercase) for i in range(10))}.mp3'
#  obj = gTTS(text=text, lang=language, slow=False)
#  obj.save(filename)
#  os.system('mpg321 ' + filename)
#  os.remove('./' + filename)
#  return '<h1>Thank you for being annoying! <3</h1>'

@app.route('/', methods=['POST'])
def poster():
  text = request.form['text'].replace('\\', '').replace('\'', '').replace('\"', '')
  if not text:
    return redirect(request.url)
  name = request.form['name']
  print(f'{request.remote_addr}|{name}> {text}')
  illegal = []
  if any(bad in text for bad in illegal):
    return f'<h1 style="font-family: sans-serif;">Wait that\'s illegal! ({", ".join(illegal)})</h1>'
  if len(text) > limit:
    return f'<h1>Message cannot exceed {limit} characters.</h1>'
  subprocess.run(['say', f'{text}{". From " + name if name else ""}'])
  return redirect(request.url)

if __name__ == '__main__':
  app.config['DEBUG'] = False
  app.run(host='0.0.0.0', port=8009)

