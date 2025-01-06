from application.model.model import User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin, get_all_the_dates
from datetime import datetime

class AllUserActivity(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append({
                "user_name": user.name,
                "user_email": user.email,
                "last_login": user.last_login_at.strftime('%d/%m/%Y %H:%M') if user.last_login_at else "--",
                "unactived_at": user.unactived_at.strftime('%d/%m/%Y %H:%M') if user.unactived_at else "--",
                "no_of_logins": user.no_of_logins,
                "status": "Active" if user.active else "Inactive"
            })
        
        return {"status": "success", "all_users_activity": users_list}, 200