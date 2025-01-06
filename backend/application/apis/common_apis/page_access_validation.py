from application.model.model import db,User, UserRole, Permission, RolePermission, Role

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity


user_page_validation_args = reqparse.RequestParser()
user_page_validation_args.add_argument(
    "page", type=str, required=True, help="Page name is required"
)

class UserPageAccessValidation(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        args = user_page_validation_args.parse_args()
        page_name = args.get('page')
        
        user = User.query.filter_by(id=current_user_id).first()
        if user is None:
            return {"status": "failed", "message": "You doesn't have permission to go this page"},200
        
        
        user_role = UserRole.query.filter_by(user_id=current_user_id).first()
        if user_role is None:
            return {"status": "failed", "message": "You doesn't have permission to go this page"},200
        
        role = Role.query.filter_by(id = user_role.role_id).first()
        if role is None:
            return {"status": "failed", "message": "You doesn't have permission to go this page"},200
        
        role_permissions = RolePermission.query.filter_by(role_id=role.id).all()
        
        for permission in role_permissions:
            per = Permission.query.filter_by(id=permission.permission_id).first()
            if per.name == page_name:
                return {"status": "success", "message": "User has access to this page"},200
        
        
        
        return {"status": "failed", "message":"You doesn't have permission to go this page"}, 200