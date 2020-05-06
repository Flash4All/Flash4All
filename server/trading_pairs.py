from flask import Blueprint, render_template, abort, jsonify, request
trading_pair_routes = Blueprint('trading_pair', __name__)

@trading_pair_routes.route('/<from_token>/<to_token>', methods=["GET", "POST", "DELETE"])
def trading_pairs_index(from_token, to_token):
    if request.method == 'GET':
        return jsonify([from_token, to_token])

