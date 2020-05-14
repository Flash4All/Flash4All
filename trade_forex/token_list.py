from flask import Blueprint, render_template, abort, jsonify, request
from redis_client import redis_client

token_routes = Blueprint('token', __name__)
addresses = {
            'MKR': '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
            'DAI': '0x6b175474e89094c44da98b954eedeac495271d0f',
            'BAT': '0x0d8775f648430679a709e98d2b0cb6250d2887ef',
            'TUSD': '0x8dd5fbce2f6a956c3022ba3663759011dd51e73e',
            'USDT': '0xdac17f958d2ee523a2206206994597c13d831ec7',
            'SAI': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
            'ETH': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
            'REP': '0xe94327d07fc17907b4db788e5adf2ed424addff6'
        }

@token_routes.route('', methods=["GET", "POST", "DELETE"])
def get_all_tokens():
    if request.method == 'GET':
        tokens = [x.decode() for x in redis_client.lrange('tokens',0, -1)]
        return jsonify(tokens)
    else:
        data = request.get_json()
        token = data.get('token', None)
        if token is None:
            return jsonify(error='token is required'), 201

        ## Make sure token isn't already reported
        tokens = [x.decode() for x in redis_client.lrange('tokens',0, -1) if x.decode() == token]

        if len(tokens) == 0:
            redis_client.lpush('tokens', token)
            return jsonify(success=1)
        else:
            return jsonify(success=0, error='token already submitted'), 201

@token_routes.route('/<token>', methods=["GET"])
def get_token_detail(token):
    if request.method == 'GET':
        return jsonify(address=addresses[token.upper()])

@token_routes.route('', methods=["POST"])
def remove_token(token):
    data = request.get_json()
    token = data.get('token', None)
    if token is None:
        return jsonify(error='token is required'), 201
