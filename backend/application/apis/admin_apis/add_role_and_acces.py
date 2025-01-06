from application.model.model import db, Role, Permission, RolePermission


from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity,jwt_required
from application.apis.helper_fun import is_admin

role_permission_post_args = reqparse.RequestParser()
role_permission_post_args.add_argument(
    "name", type=str, required=True, help="Role name is required"
)
role_permission_post_args.add_argument(
    "page_access",
    type=list,
    location="json",
    required=True,
    help="Category access is required",
)


class RolePermissionAPI(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = role_permission_post_args.parse_args()
        role_name = args.get("name")
        page_access = args.get("page_access")
        existing_role = Role.query.filter_by(name = role_name).first()
        
        if existing_role:
            return {"status": "failed", "message": "Role already exists"}, 200
        
        for page in page_access:
            permission = Permission.query.filter_by(name = page).first()
            if permission is None:
                message = page + ' not found'
                return {"status": "failed", "message": "page not found"}, 200
            
        
        new_role = Role(name = role_name, code = format_role_name(role_name))
        db.session.add(new_role)
        for page in page_access:
            permission = Permission.query.filter_by(name = page).first()
            role_permission = RolePermission(role_id = new_role.id, permission_id = permission.id)
            db.session.add(role_permission)
            
        try:
            
            db.session.commit()
            return {"status": "success", "message": "Role created"}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "message": "Not able to create role, See Logs"}, 200
        
        
def format_role_name(role_name):
    words = role_name.split()
    formatted_role_name = ''.join(word.capitalize() for word in words)
    return formatted_role_name
        
        