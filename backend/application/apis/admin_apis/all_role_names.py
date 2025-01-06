from application.model.model import db, Role
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class AllRoleNames(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        roles = Role.query.all()
        role_names = []
        for role in roles:
            role_names.append(role.code)
        return {"status": "success", "data": role_names}, 200

        
    
