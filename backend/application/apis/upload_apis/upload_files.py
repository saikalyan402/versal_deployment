from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request
import os
import shutil

relative_path = "upload_folders"
VR_PATH = "upload_folders/VR"
MFI_PATH =  "upload_folders/MFI"

class UploadFiles(Resource):
    @jwt_required()
    def post(self):
        print("Request headers:", request.headers)
        print("Request content type:", request.content_type)
        print("Request data:", request.data)
        print("Request files:", request.files)
        print("Request form:", request.form)

        
        # Check if files are in the request
        if 'files' not in request.files:
            return jsonify({'status': 'failed', 'message': 'No file part'})

        files = request.files.getlist('files')
        if not files:
            return jsonify({'status': 'failed', 'message': 'No selected files'})

        saved_files = []
        for file in files:
            if not file.filename:
                return jsonify({'status': 'failed', 'message': 'One or more files have no name'})

            file_name = file.filename
            print(f"Received file: {file_name}")

            # Determine storage path based on file name
            destination_path = VR_PATH + '/' + file_name if file_name.startswith('Birla') else MFI_PATH + '/' + file_name

            try:
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)  # Ensure directory exists
                file.save(destination_path)
                saved_files.append(destination_path)
                print(f"File saved to: {destination_path}")
            except Exception as e:
                print(f"Error saving file {file_name}: {e}")
                return jsonify({'status': 'failed', 'message': f'Failed to save file {file_name}'})

        # Ensure all files were saved
        if not all(os.path.isfile(path) for path in saved_files):
            return jsonify({'status': 'failed', 'message': 'Not all files were saved successfully'})

        return jsonify({'status': 'success', 'message': "Files saved successfully"})
