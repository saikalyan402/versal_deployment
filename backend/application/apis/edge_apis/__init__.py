import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api


from application.apis.edge_apis.edge_data import EdgePageData
from application.apis.edge_apis.edge_initial_data import EdgeInitialData



edge_api_bp = Blueprint('edge_api', __name__)
edge_api = Api(edge_api_bp, prefix='/egde/api')

edge_api.add_resource(EdgeInitialData,"/edge_init", methods=["GET"])
edge_api.add_resource(EdgePageData, "/edge_page_data", methods=["POST"])