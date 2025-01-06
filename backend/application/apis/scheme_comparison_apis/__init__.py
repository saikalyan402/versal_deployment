import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api
from flask_login import current_user



from application.apis.scheme_comparison_apis.scheme_comparison_initial_data import SchemeComparisonInitialData
from application.apis.scheme_comparison_apis.fund_overview_benchmarks import FundOverviewBenchmark
from application.apis.scheme_comparison_apis.fund_overview_compare_funds import FundOverviewCompareFunds
from application.apis.scheme_comparison_apis.fund_overview_peer_funds import FundOverviewPeerFunds

scheme_comparison_api_bp = Blueprint('scheme_comparison_api', __name__)
scheme_comparison_api = Api(scheme_comparison_api_bp, prefix='/scheme_comp/api')

scheme_comparison_api.add_resource(FundOverviewBenchmark, "/scheme_comparison_benchmark", methods = ["POST"])
scheme_comparison_api.add_resource(FundOverviewCompareFunds, "/scheme_comparison_compare_funds", methods = ["POST"])
scheme_comparison_api.add_resource(SchemeComparisonInitialData, "/scheme_comparison_init", methods =["GET"])
scheme_comparison_api.add_resource(FundOverviewPeerFunds, "/scheme_comparison_peer_funds", methods = ["POST"])

