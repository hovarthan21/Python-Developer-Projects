import os
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "md", "csv", "log", "pdf", "doc", "docx"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Receives file via multipart/form-data (from XHR).
    Returns JSON with success and filename (or error).
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part."}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file."}), 400
    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "File type not allowed."}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(save_path):
        filename = f"{base}({counter}){ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter += 1

    try:
        file.save(save_path)
    except Exception as e:
        return jsonify({"success": False, "error": f"Save failed: {str(e)}"}), 500

    return jsonify({"success": True, "filename": filename})


@app.route("/files", methods=["GET"])
def list_files():
    try:
        items = sorted(os.listdir(app.config["UPLOAD_FOLDER"]))
        files = [f for f in items if allowed_file(f)]
        return jsonify({"success": True, "files": files})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/read", methods=["POST"])
def read_file():
    """
    Expects JSON { "filename": "file.txt" }.
    Returns text content only for previewable text files.
    """
    data = request.get_json()
    filename = data.get("filename")
    if not filename or not allowed_file(filename):
        return jsonify({"success": False, "error": "Invalid filename."}), 400

    ext = filename.rsplit(".", 1)[1].lower()
    path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    if not os.path.exists(path):
        return jsonify({"success": False, "error": "File not found."}), 404

    if ext in {"txt", "md", "csv", "log"}:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return jsonify({"success": True, "content": content})
        except Exception as e:
            return jsonify({"success": False, "error": f"Read error: {str(e)}"}), 500
    else:
        return jsonify({"success": True, "content": None, "message": "Binary file (preview not available)"})


@app.route("/find_replace", methods=["POST"])
def find_replace():
    """
    Expects JSON:
    { "filename": "file.txt", "find": "apple", "replace": "orange", "replace_all": true }
    Works only for text files (txt, md, csv, log).
    """
    data = request.get_json()
    filename = data.get("filename")
    find_text = data.get("find", "")
    replace_text = data.get("replace", "")
    replace_all = bool(data.get("replace_all", True))

    if not filename or not allowed_file(filename):
        return jsonify({"success": False, "error": "Invalid filename."}), 400

    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in {"txt", "md", "csv", "log"}:
        return jsonify({"success": False, "error": "Find/Replace only supported for text files."}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    if not os.path.exists(path):
        return jsonify({"success": False, "error": "File not found."}), 404

    if find_text == "":
        return jsonify({"success": False, "error": "Find text cannot be empty."}), 400

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return jsonify({"success": False, "error": f"Read error: {str(e)}"}), 500

    if replace_all:
        replaced_count = content.count(find_text)
        new_content = content.replace(find_text, replace_text)
    else:
        if find_text in content:
            new_content = content.replace(find_text, replace_text, 1)
            replaced_count = 1
        else:
            new_content = content
            replaced_count = 0

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        return jsonify({"success": False, "error": f"Write error: {str(e)}"}), 500

    return jsonify({"success": True, "replaced": replaced_count, "content": new_content})


@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    if not allowed_file(filename):
        abort(400)
    safe_name = secure_filename(filename)
    directory = os.path.abspath(app.config["UPLOAD_FOLDER"])
    full = os.path.join(directory, safe_name)
    if not os.path.exists(full):
        abort(404)
    return send_from_directory(directory, safe_name, as_attachment=True)


@app.route("/delete", methods=["POST"])
def delete_file():
    data = request.get_json()
    filename = data.get("filename")
    if not filename:
        return jsonify({"success": False, "error": "No filename provided."}), 400
    path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    try:
        if os.path.exists(path):
            os.remove(path)
            return jsonify({"success": True, "message": "Deleted."})
        else:
            return jsonify({"success": False, "error": "File not found."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
