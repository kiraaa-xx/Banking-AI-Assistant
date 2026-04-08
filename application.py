import os
from flask import Flask, request, jsonify, render_template
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Setup logging
def setup_logging():
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

setup_logging()

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'POST':
        content = request.json
        app.logger.info(f'Received data: {content}')
        return jsonify(content), 201
    return jsonify({'message': 'GET request successful'}), 200

if __name__ == '__main__':
    db.create_all() # Create database tables
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))