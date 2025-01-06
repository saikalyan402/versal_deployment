import os
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class CheckEnvironment(Resource):
    UPLOAD_FOLDER = 'upload_folders'  # Define the main folder path

    REQUIRED_STRUCTURE = {
        "default": [
            "Debt_benchmark_values",
            "Debt_peer_set",
            "Equity_benchmark_values",
            "Equity_peer_set",
            "ETF_benchmark_values",
            "Index_benchmark_values",
            "Schemes/Debt",
            "Schemes/Equity",
            "Schemes/Index",
            "Schemes/ETF"
        ],
        "undefault": [
            "Debt_benchmark_values",
            "Debt_peer_set",
            "Equity_benchmark_values",
            "Equity_peer_set",
            "Schemes/Debt",
            "Schemes/Equity"
        ],
        "MFI": [],
        "VR": [],
        "Value_Research": []
    }

    def check_structure(self):
        """
        Checks if the required directory structure exists and ensures they are empty.
        Returns a dictionary with missing directories and non-empty folders.
        """
        issues = {}

        for main_folder, subfolders in self.REQUIRED_STRUCTURE.items():
            main_path = os.path.join(self.UPLOAD_FOLDER, main_folder)
            if not os.path.exists(main_path):
                issues[main_folder] = {"missing": True, "non_empty": False}
                continue

            # Check subfolders
            folder_issues = []
            for subfolder in subfolders:
                subfolder_path = os.path.join(main_path, subfolder)
                if not os.path.exists(subfolder_path):
                    folder_issues.append({"folder": subfolder, "missing": True, "non_empty": False})
                elif os.listdir(subfolder_path):  # Check if folder is empty
                    folder_issues.append({"folder": subfolder, "missing": False, "non_empty": True})

            if folder_issues:
                issues[main_folder] = folder_issues

        return issues

    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()

        # Check if the user is an admin
        if not is_admin(logined_user_id):
            return {"status": "failed", "message": "Only admin can access this"}, 200

        try:
            # Check the directory structure and emptiness
            issues = self.check_structure()

            if issues:
                return {
                    "status": "failed",
                    "message": "Some directories are missing or not empty",
                    "issues": issues
                }, 200

            return {"status": "success", "message": "All required directories exist and are empty"}, 200

        except Exception as e:
            return {"status": "failed", "message": f"Unexpected error: {str(e)}"}, 500
