from flask_restful import Resource,reqparse
from flask import request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.model.model import db,Category,Scheme, BenchmarkData,DailySchemePerformanceParamenter,CategoryRiskSet
from application.apis.helper_fun import schemes_data_func,categ_data
from application.apis.helper_fun import is_admin
import datetime

date_args = reqparse.RequestParser()
date_args.add_argument(
    "date", type=str, required=True, help="Date is required"
)


class DeleteData(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
         # Parse the date from the request arguments
        args = date_args.parse_args()
        delete_date = args["date"]

        # Start a session for deletion
        try:
            # Delete records from DailySchemePerformanceParamenter where performance_date matches the provided date
            db.session.query(DailySchemePerformanceParamenter).filter(DailySchemePerformanceParamenter.performance_date == delete_date).delete()

            # Delete records from CategoryRiskSet where the date field matches the provided date
            db.session.query(CategoryRiskSet).filter(CategoryRiskSet.date == delete_date).delete()

            # You can also add similar delete statements for other tables if needed (e.g., BenchmarkData)
            db.session.query(BenchmarkData).filter(BenchmarkData.date == delete_date).delete()
            # Commit the changes to the database
            db.session.commit()

            return {'status':"success","message": f"Data for {delete_date} has been deleted successfully."}, 200

        except Exception as e:
            # In case of an error, roll back the transaction and return an error message
            db.session.rollback()
            return {'status':"failed","message": str(e)}, 500