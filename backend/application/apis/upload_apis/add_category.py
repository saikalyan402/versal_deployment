from application.model.model import db, Category


from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity,jwt_required
from application.apis.helper_fun import is_admin

category_post_args = reqparse.RequestParser()
category_post_args.add_argument(
    "category_name", type=str, required=True, help="Category name is required"
)


class CategoryAPI(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = category_post_args.parse_args()
        category_name = args.get("category_name")
        
        category = Category.query.filter_by(name=category_name).first()
        if category:
            return {"status":"failed", "message":"Category already exists"}
        
        new_category = Category(name = category_name)
        
        db.session.add(new_category)
        try:    
            db.session.commit()
            return {"status": "success", "message": "Category created"}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "message": "Not able to create category, See Logs"}, 200    
          