import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api
from flask_login import current_user

from application.apis.comp_amc_apis.custom_amcOverview import CustomAMCOverviewResource
from application.apis.comp_amc_apis.amc_overview_page_data_access import AMCOverviewAccessData


amcOverview_api_bp = Blueprint('amcOverview_api', __name__)
amcOverview_api = Api(amcOverview_api_bp, prefix='/amcOverview/api')


amcOverview_api.add_resource(CustomAMCOverviewResource,"/amc_overview", methods =["POST"])
amcOverview_api.add_resource(AMCOverviewAccessData, "/amc_overview_data_access", methods = ["GET"])