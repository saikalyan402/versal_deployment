from flask_restful import Resource

from application.model.model import db,Permission

from application.apis.helper_fun import is_admin

from flask_jwt_extended import jwt_required, get_jwt_identity


class AllPermissionName(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        permissions = Permission.query.all()
        permission_names = []
        for permission in permissions:
            permission_names.append(permission.name)
            
        return {"status": "success", "data": permission_names}, 200
    
    