from application.model.model import Category, DailySchemePerformanceParamenter as performance, Scheme 
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin
from datetime import datetime
import json


fundmangerpageparser = reqparse.RequestParser()
fundmangerpageparser.add_argument(
    "category", type=str, required=True, help="category is required",
)
fundmangerpageparser.add_argument(
    "date", type=str, required=True, help="Date is required",
)

class EdgePageData(Resource):
    @jwt_required()
    def post(self):
        args = fundmangerpageparser.parse_args()
        category = args.get("category")
        date = args.get("date")
        if date:
            formated_date = datetime.strptime(date, "%Y-%m-%d").date()
        logined_user_id = get_jwt_identity()
        category_id = Category.query.filter_by(name=category).first().id
        schemes = Scheme.query.filter_by(category_id=category_id, subtype="Regular").all()
        data_list = []
        for scheme in schemes:
            perf = performance.query.filter_by(scheme_id=scheme.id, performance_date = formated_date).first()
            if perf:
                data = json.loads(perf.data)
                data_dict = {
                      "scheme_name": scheme.name,
                        "aum": data["scheme_aum"],
                        "ytd": data["YTD_return"],
                        "1d": data["one_d_return"],
                        "7d": data["seven_d_return"],
                        "14d": data["fourteen_d_return"],
                        "1m": data["thirty_d_return"],
                        "2m": data["sixty_d_return"],
                        "3m": data["ninety_d_return"],
                        "6m": data["oneeighty_d_return"],
                        "9m": data["twoseventy_d_return"],
                        "1yr": data["one_y_return"],
                        "2yr": data["two_y_return"],
                        "3yr": data["three_y_return"],
                        "4yr": data["four_y_return"],
                        "5yr": data["five_y_return"],
                        "7yr": data["seven_y_return"],
                        "10yr": data["ten_y_return"],
                        "12yr": data["twelve_y_return"],
                        "15yr": data["fifteen_y_return"],
                        "inception": data["inception_return"]
            }
                
            data_list.append(data_dict)

        data = data_list
        return {"status":"success", "data" : data}