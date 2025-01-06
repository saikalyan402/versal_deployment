from application.model.model import db, Role, Permission, RolePermission

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class AllRolePermissionAPI(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        roles = Role.query.all()
        role_permission_list = []
        for role in roles:
            new_page_list = []
            role_permissions = RolePermission.query.filter_by(role_id = role.id).all()
            for role_permission in role_permissions:
                permission = Permission.query.filter_by(id = role_permission.permission_id).first()
                new_page_list.append(permission.name)
            role_permission_list.append({
                "role": role.name,
                "role_code":role.code,
                "permissions": new_page_list
            })
        return {"status": "success", "data": role_permission_list}, 200
        