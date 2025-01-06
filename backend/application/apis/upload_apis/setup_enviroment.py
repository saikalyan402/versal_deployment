import os
import shutil
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class SetUpEnvironment(Resource):
    UPLOAD_FOLDER = 'upload_folders'  # Define the main folder path

    def create_subdirectories(self, base_path, subdirectories, scheme_subfolders=None):
        """
        Helper function to create subdirectories and optionally add specific subfolders under 'Scheme'.
        """
        try:
            for subdirectory in subdirectories:
                path = os.path.join(base_path, subdirectory)
                os.makedirs(path, exist_ok=True)  # Ensure the folder is created only if it doesn't already exist

                # Add specific folders under 'Scheme'
                if scheme_subfolders and subdirectory == 'Schemes':
                    for scheme_subfolder in scheme_subfolders:
                        os.makedirs(os.path.join(path, scheme_subfolder), exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create subdirectories at {base_path}: {str(e)}")

    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()

        # Check if the user is an admin
        if not is_admin(logined_user_id):
            return {"status": "failed", "message": "Only admin can access this"}, 200

        try:
            # Step 1: Remove the 'upload_folders' directory if it exists
            if os.path.exists(self.UPLOAD_FOLDER):
                shutil.rmtree(self.UPLOAD_FOLDER)

            # Step 2: Recreate the main 'upload_folders' directory
            os.makedirs(self.UPLOAD_FOLDER)

            # Step 3: Create main subdirectories
            main_subdirectories = ['default', 'MFI', 'undefault', 'VR', 'Value_Research']
            self.create_subdirectories(self.UPLOAD_FOLDER, main_subdirectories)

            # Step 4: Create subdirectories for 'default'
            default_subdirectories = [
                'Debt_benchmark_values',
                'Debt_peer_set',
                'Equity_benchmark_values',
                'Equity_peer_set',
                'ETF_benchmark_values',
                'Index_benchmark_values',
                'Schemes'
            ]
            default_scheme_subfolders = ['Debt', 'Equity', 'Index', 'ETF']
            self.create_subdirectories(
                os.path.join(self.UPLOAD_FOLDER, 'default'), 
                default_subdirectories, 
                scheme_subfolders=default_scheme_subfolders
            )

            # Step 5: Create subdirectories for 'undefault'
            undefault_subdirectories = [
                'Debt_benchmark_values',
                'Debt_peer_set',
                'Equity_benchmark_values',
                'Equity_peer_set',
                'Schemes'
            ]
            undefault_scheme_subfolders = ['Debt', 'Equity']
            self.create_subdirectories(
                os.path.join(self.UPLOAD_FOLDER, 'undefault'), 
                undefault_subdirectories, 
                scheme_subfolders=undefault_scheme_subfolders
            )

            return {"status": "success", "message": "Environment set up successfully"}, 200

        except RuntimeError as re:
            return {"status": "failed", "message": str(re)}, 500

        except Exception as e:
            return {"status": "failed", "message": f"Unexpected error: {str(e)}"}, 500
