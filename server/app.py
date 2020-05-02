from flask import Flask, jsonify, request
import settings

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(success=1)

