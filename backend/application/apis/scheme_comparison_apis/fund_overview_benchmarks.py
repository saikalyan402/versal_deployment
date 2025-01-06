from flask_restful import Resource, reqparse
from flask import jsonify
from application.apis.helper_fun import schemes_data_func,landing_peer,landing_scheme_beat,landing_scheme_beat_new,get_all_the_dates
from datetime import datetime,timedelta
from application.model.model import Benchmark, BenchmarkData
from flask_jwt_extended import jwt_required,get_jwt_identity
import json



scheme_comparison_benchmark_selector = reqparse.RequestParser()
scheme_comparison_benchmark_selector.add_argument(
    "benchmarkname", type=str, required=True, help="Benchmark is required",
)
scheme_comparison_benchmark_selector.add_argument(
    "date", type=str, required=True, help="Date is required",
)

class FundOverviewBenchmark(Resource):
    @jwt_required()
    def post(self):
        args = scheme_comparison_benchmark_selector.parse_args()
        benchmark_name = args.get("benchmarkname")
        date = args.get("date")

        try:
            if date:
                # Formatting the date
                formated_date = datetime.strptime(date, "%Y-%m-%d").date()

            # Fetch the benchmark based on name
            benchmark_id = Benchmark.query.filter_by(name=benchmark_name).first()

            if benchmark_id:
                # Fetch the benchmark data for the specific date
                benchmark_data = BenchmarkData.query.filter_by(benchmark_id=benchmark_id.id, date=formated_date).first()

                # Check if benchmark data exists
                if benchmark_data:
                    # If data is found, parse the JSON data
                    try:
                        bench = json.loads(benchmark_data.data)
                    except json.JSONDecodeError:
                        return {"status": "error", "message": "Failed to decode benchmark data."}, 400

                    # Preparing benchmark data dictionary
                    benchmark_data_dict = {
                        "bench_name": benchmark_name,
                        "ytd": bench.get("YTD"),
                        "1d": bench.get("one_d"),
                        "7d": bench.get("seven_d"),
                        "14d": bench.get("fourteen_d"),
                        "1m": bench.get("thirty_d"),
                        "2m": bench.get("sixty_d"),
                        "3m": bench.get("ninety_d"),
                        "6m": bench.get("oneeighty_d"),
                        "9m": bench.get("twoseventy_d"),
                        "1yr": bench.get("one_y"),
                        "2yr": bench.get("two_y"),
                        "3yr": bench.get("three_y"),
                        "4yr": bench.get("four_y"),
                        "5yr": bench.get("five_y"),
                        "7yr": bench.get("seven_y"),
                        "10yr": bench.get("ten_y"),
                        "12yr": bench.get("twelve_y"),
                        "15yr": bench.get("fifteen_y"),
                        "20yr": bench.get("twenty_y")
                    }

                    # Returning the benchmark data
                    data = {
                        "benchmark_data": benchmark_data_dict
                    }
                    return {"status": "success", "data": data}, 200

                else:
                    # Handle case where no benchmark data is found for the given date
                    return {"status": "error", "message": "Benchmark data not found for the specified date."}, 404
            else:
                # Handle case where benchmark name doesn't exist in the database
                return {"status": "error", "message": "Benchmark not found."}, 404

        except Exception as e:
            # General error handling
            return {"status": "error", "message": str(e)}, 500