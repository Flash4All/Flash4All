from flask import Blueprint, render_template, abort, jsonify, request
from redis_client import redis_client

token_routes = Blueprint('token', __name__)

@token_routes.route('', methods=["GET", "POST", "DELETE"])
def get_all_tokens():
    if request.method == 'GET':
        tokens = [x.decode() for x in redis_client.lrange('tokens',0, -1)]
        return jsonify(tokens)
    else:
        data = request.get_json()
        token = data.get('token', None)
        print(token)
        if token is None:
            return jsonify(error='token is required'), 201

        ## Make sure token isn't already reported
        tokens = [x.decode() for x in redis_client.lrange('tokens',0, -1) if x.decode() == token]

        if len(tokens) == 0:
            redis_client.lpush('tokens', token)
            return jsonify(success=1)
        else:
            return jsonify(success=0, error='token already submitted'), 201

