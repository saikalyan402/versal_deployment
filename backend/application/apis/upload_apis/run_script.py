from flask import Response, stream_with_context
from flask_restful import Resource
from flask_jwt_extended import jwt_required

import os

from application.apis.upload_apis.helpers.upload_helper_func import unprotect_files, read_files, fun
from application.apis.upload_apis.helpers.populate_benchmark import populate_benchmark
from application.apis.upload_apis.helpers.populate_scheme import populate_scheme
from application.apis.upload_apis.helpers.populate_peer_average import populate_peer
from application.apis.upload_apis.helpers.populate_scheme_performance_daily import populate_perf

curr_dir = os.getcwd() + '/upload_folders/'

class RunAddToDatabaseScript(Resource):
    @jwt_required()
    def get(self):
        def execute_script():
            try:
                yield "Starting the script...\n"
                unprotect_files(curr_dir)
                fles, new_date, first_col = fun(curr_dir)
                yield f"step_1_completed: Files unprotected and processed\n"
            except Exception as e:
                yield f"error_in_step_1: {str(e)}\n"
                return
            
            try:
                read_files(curr_dir, fles, first_col)
                yield "step_2_completed: Files read successfully.\n"
            except Exception as e:
                yield f"error_in_step_2: {str(e)}\n"
                return
            
            try:
                status, message = populate_scheme(curr_dir, first_col)
                if status == "successful":
                    yield "step_3_completed: Scheme populated.\n"
                else:
                    yield str(status) + ": " + str(message)
                    return
            except Exception as e:
                yield f"error_in_step_3: {str(e)}\n"
                return
            
            try:
                populate_benchmark(curr_dir, new_date, first_col)
                yield "step_4_completed: Benchmark populated.\n"
            except Exception as e:
                yield f"error_in_step_4: {str(e)}\n"
                return
            
            try:
                populate_peer(curr_dir, new_date, first_col)
                yield "step_5_completed: Peer average populated.\n"
            except Exception as e:
                yield f"error_in_step_5: {str(e)}\n"
                return
            
            try:
                populate_perf(curr_dir, new_date, first_col)
                yield "step_6_completed: Performance data populated.\n"
            except Exception as e:
                yield f"error_in_step_6: {str(e)}\n"
                return
            
            yield "Script executed successfully.\n"

        return Response(stream_with_context(execute_script()), content_type='text/plain')
