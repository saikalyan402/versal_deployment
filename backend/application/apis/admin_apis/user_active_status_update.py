from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin
from application.model.model import db , User
from datetime import datetime

user_input_validation = reqparse.RequestParser()

user_input_validation.add_argument(
    "email", type=str, required=True, help="email is required",
)

class UserActiveStatus(Resource):
    @jwt_required()
    def patch(self):
        args = user_input_validation.parse_args()
        user_activity = args.get("activity_status")
        user_email = args.get("email")
        
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return {"status":"failed","message":"User is not found"},404 

        
        if user.active==1:
            user.active = 0
            user.unactived_at = datetime.now()
            db.session.commit()
            return {"status":"success","message":f"{user.name} deactivated"},200
        
        if user.active==0:
            user.active = 1
            user.last_login_at = datetime.now()
            user.unactived_at = None
            db.session.commit()
            return {"status":"success","message":f"{user.name} activated"},200
        

        return {"status":"failed", "message":"unexpeceted Error Occur"}