import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api
from flask_login import current_user

from application.apis.upload_apis.setup_enviroment import SetUpEnvironment
from application.apis.upload_apis.check_enviroment import CheckEnvironment
from application.apis.upload_apis.upload_files import UploadFiles
from application.apis.upload_apis.run_script import RunAddToDatabaseScript
from application.apis.upload_apis.add_category import CategoryAPI
from application.apis.upload_apis.add_company import CompanyAPI


upload_api_bp = Blueprint('upload_api', __name__)
upload_api = Api(upload_api_bp, prefix='/upload/api')


GPPP = ["GET", "POST", "PUT", "PATCH"]
upload_api.add_resource(SetUpEnvironment, '/setup_env', methods=["GET"])
upload_api.add_resource(CheckEnvironment, '/check_env', methods=["GET"])
upload_api.add_resource(UploadFiles, '/save_files', methods = ["POST"])
upload_api.add_resource(RunAddToDatabaseScript, '/add_to_db', methods = ["GET"])
upload_api.add_resource(CategoryAPI, "/add_category", methods = ["POST"])
upload_api.add_resource(CompanyAPI, "/add_company", methods = ["POST"])