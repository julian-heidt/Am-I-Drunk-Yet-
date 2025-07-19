from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    api_url = os.environ.get('API_URL', 'http://localhost:8080')
    return render_template('index.html', api_url=api_url)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 