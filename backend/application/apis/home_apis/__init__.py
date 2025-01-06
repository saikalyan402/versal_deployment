import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api
from flask_login import current_user



from application.apis.home_apis.custom_landing_peer import LandingAPI
from application.apis.home_apis.home_beating_benchmark_graph import HomeBenchBeatChart
from application.apis.home_apis.home_initial_data import HomeInitialData


home_api_bp = Blueprint('home_api', __name__)
home_api = Api(home_api_bp, prefix='/home/api')


home_api.add_resource(LandingAPI, '/landing', methods=["POST"])
home_api.add_resource(HomeBenchBeatChart, "/home_bench_beat_chart",methods=["POST"])
home_api.add_resource(HomeInitialData, "/home_init", methods =["GET"])
