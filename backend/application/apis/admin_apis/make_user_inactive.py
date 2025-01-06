from application.model.model import db, User

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

user_inactive_post_args = reqparse.RequestParser()
user_inactive_post_args.add_argument(
    "email", type=str, required=True, help="User mail is required"
)

class MakeUserInactive(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = user_inactive_post_args.parse_args()
        email = args.get("email")
        
        user = User.query.filter_by(email= email).first()
        if user is None:
            return {"status":"failed", "message":"User not found"}, 200
        user.active = False
        try:
            db.session.commit()
            return {"status": "success", "message": "User is now inactive"}, 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"status": "failed", "message": "Faield to make user inactive" }