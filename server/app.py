from flask import Flask, jsonify, request
from redis_client import redis_client
import settings


## ROUTES
from trading_pairs import trading_pair_routes
from tokens import token_routes

## Create Application
app = Flask(__name__)

## Register subroutes
app.register_blueprint(token_routes, url_prefix='/tokens')
app.register_blueprint(trading_pair_routes, url_prefix='/pairs')

@app.route('/')
def index():
    redis = redis_client
    value = redis.set('fff', 2, 5)
    value = redis.get('fff')
    print(value)
    return jsonify(success=value.decode())
