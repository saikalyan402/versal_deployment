from application.model.model import Role, Permission, RolePermission, db

from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin


role_page_post_args = reqparse.RequestParser()
role_page_post_args.add_argument(
    "role_code", type=str, required=True, help="role name is required"
)
role_page_post_args.add_argument(
    "page_access",
    type=list,
    location="json",
    required=True,
    help="page access is required",
)

class EditRolePageAccess(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = role_page_post_args.parse_args()
        
        role_code = args.get("role_code")
        page_access = args.get("page_access")
        
        role = Role.query.filter_by(code = role_code).first()
        
        if role is None:
            return {"status": "failed", "message":"role not found"}
        
        previous_access = RolePermission.query.filter_by(role_id = role.id).all()
        
        if previous_access:
            for access in previous_access:
                try:
                    db.session.delete(access)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return {"status": "failed", "message":"error in deleting previous access, contact a developer"}
                
        for access in page_access:
            permission = Permission.query.filter_by(name = access).first()
            
            new_role_permission = RolePermission(role_id = role.id, permission_id = permission.id)
            
            try:
                db.session.add(new_role_permission)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
        
        
        return {"status":"success", "message": "role page access updated"}