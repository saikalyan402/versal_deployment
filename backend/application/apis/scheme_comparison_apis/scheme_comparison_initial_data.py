from application.model.model import db, Benchmark, Category, UserCategoryAccess,Role,Company, Scheme

from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.apis.helper_fun import get_all_the_dates


class SchemeComparisonInitialData(Resource):
    @jwt_required()
    def get(self):
        current_user =  get_jwt_identity()
        current_user_id = current_user


        user_cat_access = UserCategoryAccess.query.filter_by(user_id = current_user_id).all()
        user_category_ids =[]
        for cat in user_cat_access:
            user_category_ids.append(cat.category_id)
        type_category_amc_mapping ={}

        schemes = Scheme.query.filter(Scheme.category_id.in_(user_category_ids)).all()

        for scheme in schemes:
            if scheme.subtype not in type_category_amc_mapping.keys():
                type_category_amc_mapping[scheme.subtype] = {}

            if scheme.type not in type_category_amc_mapping[scheme.subtype].keys():
                type_category_amc_mapping[scheme.subtype][scheme.type] = {}

            amc_name = Company.query.filter_by(id = scheme.company_id).first().name
            if  amc_name not in type_category_amc_mapping[scheme.subtype][scheme.type].keys():
                type_category_amc_mapping[scheme.subtype][scheme.type][amc_name] = []
            
            category_name = Category.query.filter_by(id = scheme.category_id).first().name
            if category_name not in type_category_amc_mapping[scheme.subtype][scheme.type][amc_name]:
                type_category_amc_mapping[scheme.subtype][scheme.type][amc_name].append(category_name)
        
        benchmarks = Benchmark.query.all()
        all_benchmarks = set()
        for benchmark_name in benchmarks:
            all_benchmarks.add(benchmark_name.name)

        data = {
            "type_category_amc_mapping" : type_category_amc_mapping,
            "all_dates" : get_all_the_dates(),
            "all_benchmarks" : sorted(all_benchmarks)
        }
        
        return {"status": "success", "data": data}, 200