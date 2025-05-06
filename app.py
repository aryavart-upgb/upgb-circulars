import os
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PDF_FOLDER = "pdfs"
pdf_index = []

# Load PDF content
for filename in os.listdir(PDF_FOLDER):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(PDF_FOLDER, filename)
        try:
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            pdf_index.append({
                "name": filename,
                "file": f"/{PDF_FOLDER}/{filename}",
                "content": text.lower()
            })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

@app.route("/search")
def search():
    keyword = request.args.get("q", "").lower()
    result = [pdf for pdf in pdf_index if keyword in pdf["content"] or keyword in pdf["name"].lower()]
    return jsonify(result)

@app.route("/")
def home():
    return "UPGB PDF Search API Running"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

