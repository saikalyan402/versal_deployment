from flask_restful import Resource, reqparse
from flask import jsonify
from application.apis.helper_fun import schemes_data_func,landing_peer,landing_scheme_beat,landing_scheme_beat_new,get_all_the_dates
from datetime import datetime,timedelta
from application.model.model import DailySchemePerformanceParamenter as Performance, Scheme, Company, Category
from flask_jwt_extended import jwt_required,get_jwt_identity
import json
 
 
 
scheme_comparison_first_selector = reqparse.RequestParser()
scheme_comparison_first_selector.add_argument(
    "subtype", type=str, required=True, help="Subtype is required",
)
scheme_comparison_first_selector.add_argument(
    "type", type=str, required=True, help="Type is required",
)
scheme_comparison_first_selector.add_argument(
    "amc", type=str, required=True, help="AMC is required",
)
scheme_comparison_first_selector.add_argument(
    "category", type=str, required=True, help="category is required",
)
scheme_comparison_first_selector.add_argument(
    "date", type=str, required=True, help="Date is required",
)
 
class FundOverviewCompareFunds(Resource):
    @jwt_required()
    def post(self):
        args = scheme_comparison_first_selector.parse_args()
        subtype = args.get("subtype")
        type = args.get("type")
        amc = args.get("amc")
        category = args.get("category")
        date = args.get("date")
 
        if date:
            formated_date = datetime.strptime(date, "%Y-%m-%d").date()
 
 
        company = Company.query.filter_by(name = amc).first()
        if company is None:
            return {"status":"failed","message":"AMC not found"}, 404
       
        company_id = company.id
       
        category = Category.query.filter_by(name = category).first()
        if category is None:
            return {"status":"failed","message":"category not found"}, 404
 
        category_id = category.id
        customized_risk_set = category.customised_risk_set
        scheme = Scheme.query.filter_by(category_id = category_id, company_id = company_id, subtype = subtype, type = type).first()
        if scheme is None:
            return {"status":"failed","message":"Scheme not found"}, 404
        perf = Performance.query.filter_by(scheme_id = scheme.id, performance_date = formated_date).first()
        scheme_data ={}
        if perf:
            data = json.loads(perf.data)
            scheme_data = {
                  "return":{
                        "name": scheme.name,
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
            }}
       
        data = {
            "scheme_data": scheme_data
        }
        return{"status": "success", "data": data}    
