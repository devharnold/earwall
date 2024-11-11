# app views
from flask import Blueprint, request, jsonify
from apis.v1.graphql.schema import schema

graphql_bp = Blueprint('graphql_bp', __name__)

@graphql_bp.route("graphql", methods=['POST'])
def graphql_server():
    data = request.get_json()
    result = schema.execute(data.get('query'), variables=data.get('variables'))
    if result.errors:
        return jsonify({'errors': [str(error) for error in result.errors]}), 400
    return jsonify(result.data)
