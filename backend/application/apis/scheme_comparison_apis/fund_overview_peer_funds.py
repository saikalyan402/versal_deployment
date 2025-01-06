from flask_restful import Resource, reqparse
from flask import jsonify
from application.apis.helper_fun import schemes_data_func,landing_peer,landing_scheme_beat,landing_scheme_beat_new,get_all_the_dates
from datetime import datetime,timedelta
from application.model.model import DailySchemePerformanceParamenter as Performance, CategoryRiskSet, Scheme, Company, Benchmark, BenchmarkConfig, BenchmarkData, Category
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


class FundOverviewPeerFunds(Resource):
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
        customized_risk_set = []
        risk_set_company_id = category.customised_risk_set
        for company_id in risk_set_company_id:
            scheme = Scheme.query.filter_by(company_id = company_id, category_id = category_id, type = type, subtype = subtype).first()
            if scheme:
                customized_risk_set.append(scheme.id)
                
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
            }, 
            "rank": {   
                        "name": scheme.name,
                        "ytd": data["YTD_rank"],
                        "1d": data["one_d_rank"],
                        "7d": data["seven_d_rank"],
                        "14d": data["fourteen_d_rank"],
                        "1m": data["thirty_d_rank"],
                        "2m": data["sixty_d_rank"],
                        "3m": data["ninety_d_rank"],
                        "6m": data["oneeighty_d_rank"],
                        "9m": data["twoseventy_d_rank"],
                        "1yr": data["one_y_rank"],
                        "2yr": data["two_y_rank"],
                        "3yr": data["three_y_rank"],
                        "4yr": data["four_y_rank"],
                        "5yr": data["five_y_rank"],
                        "7yr": data["seven_y_rank"],
                        "10yr": data["ten_y_rank"],
                        "12yr": data["twelve_y_rank"],
                        "15yr": data["fifteen_y_rank"],
                        "inception": data["inception_rank"]
                    }}

        benchmark_data_dict ={}
        benchmark_config = BenchmarkConfig.query.filter_by(category_id = category_id).first()
        if benchmark_config:
            benchmark =  Benchmark.query.filter_by(name = benchmark_config.benchmark_name).first()
            
            if benchmark:
                benchmark_data = BenchmarkData.query.filter_by(benchmark_id = benchmark.id, date = formated_date).first()
                bench = json.loads(benchmark_data.data)
                benchmark_data_dict = {
                        "bench_name": benchmark.name,
                        "ytd": bench["YTD"],
                        "1d": bench["one_d"],
                        "7d": bench["seven_d"],
                        "14d": bench["fourteen_d"],
                        "1m": bench["thirty_d"],
                        "2m": bench["sixty_d"],
                        "3m": bench["ninety_d"],
                        "6m": bench["oneeighty_d"],
                        "9m": bench["twoseventy_d"],
                        "1yr": bench["one_y"],
                        "2yr": bench["two_y"],
                        "3yr": bench["three_y"],
                        "4yr": bench["four_y"],
                        "5yr": bench["five_y"],
                        "7yr": bench["seven_y"],
                        "10yr": bench["ten_y"],
                        "12yr": bench["twelve_y"],
                        "15yr": bench["fifteen_y"],
                        "20yr": bench["twenty_y"]
                }
            
    
        peer_avg_data ={}
        peer_avg = CategoryRiskSet.query.filter_by(category_id = category_id, type = type, subtype = subtype).first()
        risk_set = peer_avg.risk_set
        if peer_avg:
            peer = json.loads(peer_avg.data)
            peer_avg_data = {
                    "ytd": peer["YTD"],
                    "1d": peer["one_d"],
                    "7d": peer["seven_d"],
                    "14d": peer["fourteen_d"],
                    "1m": peer["thirty_d"],
                    "2m": peer["sixty_d"],
                    "3m": peer["ninety_d"],
                    "6m": peer["oneeighty_d"],
                    "9m": peer["twoseventy_d"],
                    "1yr": peer["one_y"],
                    "2yr": peer["two_y"],
                    "3yr": peer["three_y"],
                    "4yr": peer["four_y"],
                    "5yr": peer["five_y"],
                    "7yr": peer["seven_y"],
                    "10yr": peer["ten_y"],
                    "12yr": peer["twelve_y"],
                    "15yr": peer["fifteen_y"],
                    "inception": peer["inception"]
            }
        peers_data = {}
        schemes = Scheme.query.filter_by(category_id=category_id,subtype = subtype, type = type).all()
        for scheme in schemes:
            scheme_name = scheme.name
            perf = Performance.query.filter_by(scheme_id = scheme.id, performance_date = formated_date).first()
            if perf:
                data = json.loads(perf.data)
                category_peer_data = {
                    "return":{
                        "id": scheme.id,
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
                        "inception": data["inception_return"]}, 
                    "rank": {
                        "id": scheme.id,
                        "ytd": data["YTD_rank"],
                        "1d": data["one_d_rank"],
                        "7d": data["seven_d_rank"],
                        "14d": data["fourteen_d_rank"],
                        "1m": data["thirty_d_rank"],
                        "2m": data["sixty_d_rank"],
                        "3m": data["ninety_d_rank"],
                        "6m": data["oneeighty_d_rank"],
                        "9m": data["twoseventy_d_rank"],
                        "1yr": data["one_y_rank"],
                        "2yr": data["two_y_rank"],
                        "3yr": data["three_y_rank"],
                        "4yr": data["four_y_rank"],
                        "5yr": data["five_y_rank"],
                        "7yr": data["seven_y_rank"],
                        "10yr": data["ten_y_rank"],
                        "12yr": data["twelve_y_rank"],
                        "15yr": data["fifteen_y_rank"],
                        "inception": data["inception_rank"]
                            }}
                if scheme_name not in peers_data.keys():
                    peers_data[scheme_name] = category_peer_data
        
       

        data = {
            "scheme_data":scheme_data,
            "peers_data":peers_data,
            "peer_avg": peer_avg_data,
            "benchmark_data": benchmark_data_dict,
            "risk_set":risk_set,
            "customized_risk_set": customized_risk_set
        }

        return {"status":"success", "data" : data}