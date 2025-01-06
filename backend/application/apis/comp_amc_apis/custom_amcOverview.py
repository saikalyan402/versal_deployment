import json
from datetime import datetime,timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.model.model import UserCategoryAccess
from application.model.model import (
    db,
    Company,
    Scheme,
    Category,
    DailySchemePerformanceParamenter,

)
from flask import jsonify


comp_scheme = {}
perf_schem = {}

amc_overview_get_args = reqparse.RequestParser()
amc_overview_get_args.add_argument(
    "subtype", type=str, required=True, help="Subtype is required",
)
amc_overview_get_args.add_argument(
    "type", type=str, required=True, help="Type is required",
)
amc_overview_get_args.add_argument(
    "date", type=str, required=True, help="Date is required",
)
amc_overview_get_args.add_argument(
    "amc1", type=str, required=True, help="AMC is required",
)


class CustomAMCOverviewResource(Resource):
    @jwt_required()
    def post(self):
        args = amc_overview_get_args.parse_args()
        subtype = args.get("subtype")
        type = args.get("type")
        date = args.get("date")[:10]  #2024-07-03
        # date = args.get("date")
        amc1 = args.get("amc1")
        
        formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
        # date_previous = '2024-07-04'
        
        current_user =  get_jwt_identity()
        current_user_id = current_user
        user_cat_access = UserCategoryAccess.query.filter_by(user_id = current_user_id).all()
        user_category_ids =[]
        for cat in user_cat_access:
            user_category_ids.append(cat.category_id)
        try:
            schemes_all = []
            for category_id in user_category_ids:
                schemes = Scheme.query.filter_by(
                    category_id=category_id , type = type, subtype = subtype
                ).all()
                for product in schemes:
                    company_id = product.company_id
                    schemes_all.append(product)
            for scheme in schemes_all:
                performances = DailySchemePerformanceParamenter.query.filter_by(
                    scheme_id=scheme.id, performance_date=formatted_date
                ).all()
                for perf in performances:
                    scheme_subtype = scheme.subtype
                    scheme_type = scheme.type
                    category_id = scheme.category_id                        
                    category = Category.query.filter_by(id=category_id).first().name
                    scheme_name = scheme.name
                    company_id = scheme.company_id
                    company_name = Company.query.filter_by(id=company_id).first().name

                    perf_data = json.loads(perf.data)

                    performance_values_return = [
                        perf_data["YTD_return"],
                        perf_data["one_d_return"],
                        perf_data["seven_d_return"],
                        perf_data["fourteen_d_return"],
                        perf_data["thirty_d_return"],
                        perf_data["sixty_d_return"],
                        perf_data["ninety_d_return"],
                        perf_data["oneeighty_d_return"],
                        perf_data["twoseventy_d_return"],
                        perf_data["one_y_return"],
                        perf_data["two_y_return"],
                        perf_data["three_y_return"],
                        perf_data["four_y_return"],
                        perf_data["five_y_return"],
                        perf_data["seven_y_return"],
                        perf_data["ten_y_return"],
                        perf_data["twelve_y_return"],
                        perf_data["fifteen_y_return"],
                        perf_data["inception_return"]
                    ]

                    performance_values_rank = [
                        perf_data["YTD_rank"],
                        perf_data["one_d_rank"],
                        perf_data["seven_d_rank"],
                        perf_data["fourteen_d_rank"],
                        perf_data["thirty_d_rank"],
                        perf_data["sixty_d_rank"],
                        perf_data["ninety_d_rank"],
                        perf_data["oneeighty_d_rank"],
                        perf_data["twoseventy_d_rank"],
                        perf_data["one_y_rank"],
                        perf_data["two_y_rank"],
                        perf_data["three_y_rank"],
                        perf_data["four_y_rank"],
                        perf_data["five_y_rank"],
                        perf_data["seven_y_rank"],
                        perf_data["ten_y_rank"],
                        perf_data["twelve_y_rank"],
                        perf_data["fifteen_y_rank"],
                        perf_data["inception_rank"]
                    ]
                    if scheme_subtype not in comp_scheme:
                        comp_scheme[scheme_subtype] = {}
                    if scheme_type not in comp_scheme[scheme_subtype]:
                        comp_scheme[scheme_subtype][scheme_type] = {}
                    if company_name not in comp_scheme[scheme_subtype][scheme_type]:
                        comp_scheme[scheme_subtype][scheme_type][company_name] = {}
                    
                    if (
                        category
                        not in comp_scheme[scheme_subtype][scheme_type][company_name]
                    ):
                        comp_scheme[scheme_subtype][scheme_type][company_name][
                            category
                        ] = {}
                    if scheme_name not in comp_scheme[scheme_subtype][scheme_type][company_name][category]:
                        comp_scheme[scheme_subtype][scheme_type][company_name][category][scheme_name] = ""
                       

                    if scheme_name not in perf_schem:
                        perf_schem[scheme_name] = {}
                    perf_schem[scheme_name][str(perf.performance_date)] = {
                        "aum": perf_data["scheme_aum"],
                        "return": performance_values_return,
                        "rank": performance_values_rank,
                    }
            data = {
                "comp_schem": comp_scheme,
                "perf_schem": perf_schem,
            }

            return jsonify(data)

        except Exception as e:
            return jsonify({"message": str(e)}), 500