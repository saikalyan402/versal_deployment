from application.model.model import db, Company


from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity,jwt_required
from application.apis.helper_fun import is_admin

company_post_args = reqparse.RequestParser()
company_post_args.add_argument(
    "company_name", type=str, required=True, help="Company name is required"
)


class CompanyAPI(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = company_post_args.parse_args()
        company_name = args.get("company_name")
        
        company = Company.query.filter_by(name=company_name).first()
        if company:
            return {"status":"failed", "message":"Company already exists"}
        
        new_company = Company(name = company_name)
        
        db.session.add(new_company)
        try:    
            db.session.commit()
            return {"status": "success", "message": "Company created"}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "message": "Not able to create company, See Logs"}, 200    
          