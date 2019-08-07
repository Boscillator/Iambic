from flask import Flask
from flask import redirect, url_for

app = Flask(__name__, static_url_path='/app/')

@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='index.html'))


if __name__ == '__main__':
    app.run()
