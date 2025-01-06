import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api, Resource
from flask_login import current_user
import os

from .role import RoleResource, RolesResource
from .user import UserResource, UsersResource
from .user_role import UserRoleResource, UserRolesResource
from .company import CompanyResource, CompanysResource
from .category import CategoryResource, CategorysResource
from .permission import PermissionResource, PermissionsResource

db_api_bp = Blueprint('db_api', __name__)
db_api = Api(db_api_bp, prefix='/db_api')

env = os.getenv("ENV", "production")


SECRET_KEY = os.getenv('SECRET_KEY')


@db_api_bp.before_request
def check_user():
    """Checks if the user is authenticated with role admin"""
    if request.endpoint == "api.specs":
        if not current_user.is_authenticated:
            abort(401)
        if not (
            set(["ADMIN"])
            & set(map(lambda x: x.code, current_user.roles))
        ):
            abort(403)
        return

    if "x-api-key" not in request.headers:
        return {"meta": {"status": "error"}, "data": {"message": "Token required"}}, 401

    token = request.headers["x-api-key"]

    try:
        jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        return {"meta": {"status": "error"}, "data": {"message": "Token has expired"}}, 401
    except jwt.InvalidTokenError:
        return {"meta": {"status": "error"}, "data": {"message": "Invalid token"}}, 401

class ApiDocs(Resource):
    def get(self):
        return {
            "meta": {"version": "v1", "status": "success"},
            "data": {"message": "Welcome to the API"},
        }
    


GPPP = ["GET", "POST", "PUT", "PATCH"]
db_api.add_resource(ApiDocs, "/")
db_api.add_resource(RoleResource, '/role', methods=GPPP)
db_api.add_resource(RolesResource, '/roles', methods=["GET"])
db_api.add_resource(UserResource, '/user', methods=GPPP)
db_api.add_resource(UsersResource, '/users', methods=["GET"])
db_api.add_resource(UserRoleResource, '/user_role', methods=GPPP)
db_api.add_resource(UserRolesResource, '/user_roles', methods=["GET"])
db_api.add_resource(CompanyResource, '/company', methods=GPPP)
db_api.add_resource(CompanysResource, '/companys', methods=["GET"])
db_api.add_resource(CategoryResource, '/category', methods=GPPP)
db_api.add_resource(CategorysResource, '/categorys', methods=["GET"])
db_api.add_resource(PermissionResource, '/permission', methods=GPPP)
db_api.add_resource(PermissionsResource, '/permissions', methods=["GET"])
