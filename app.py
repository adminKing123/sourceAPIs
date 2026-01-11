from flask import Flask, request, jsonify
from flask_cors import CORS
from config import CONFIG
from files import utils as files

app = Flask(__name__)
CORS(app)

@app.route("/download/<path:file_path_o>")
def download(file_path_o):
    return files.download_file_stream(file_path_o)

@app.route("/upload_file", methods=["POST"])
def upload_file():
    user_id = request.form.get("user_id")
    file_id = request.form.get("file_id")
    file_type = request.form.get("file_type", "")

    if not user_id or not file_id:
        return jsonify({"error": "user_id and file_id are required"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_meta = files.save_file(file, user_id, file_id, file_type)

    return jsonify(file_meta), 201

@app.route("/delete_file/<filename>", methods=["DELETE"])
def delete_file(filename):
    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # GitHub repo path (same as upload logic)
    file_path_o = f"{CONFIG.UPLOAD1.UPLOAD_FOLDER}/{user_id}/{filename}"
    print(file_path_o)
    commit_message = f"Delete file {filename} for user {user_id}"

    success = files.remove_file(
        file_path=file_path_o,
        commit_message=commit_message
    )

    if not success:
        return jsonify({"error": "File not found or delete failed"}), 404

    return jsonify({
        "success": True,
        "message": "File deleted successfully"
    }), 200

app.run(host='0.0.0.0', port=CONFIG.PORT, debug=CONFIG.DEBUG)