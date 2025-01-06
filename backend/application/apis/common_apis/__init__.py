import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api


from application.apis.common_apis.user_login import UserLogin
from application.apis.common_apis.page_access_validation import UserPageAccessValidation

common_api_bp = Blueprint('common_api', __name__)
common_api = Api(common_api_bp, prefix='/api')


GPPP = ["GET", "POST", "PUT", "PATCH"]
common_api.add_resource(UserLogin,"/login", methods = ["POST"])
common_api.add_resource(UserPageAccessValidation, "/check_page_access", methods = ["POST"])
