import os
import fitz  # PyMuPDF
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://upgb-circulars-backend.onrender.com"])


# Folder to store the PDFs (adjust this to your actual path)
PDFS_DIRECTORY = "pdfs"  # Make sure PDFs are uploaded to this directory

# Static list of circulars from your index.html
pdfs = [
    {"name": "Circular 1 - Discretionary Administrative Powers- Cancelled", "file": "Circular No. 01 dated 01.05.2025.pdf"},
    {"name": "Circular 2 - Appointment of Chairman Sir", "file": "Cir No. 02 - Chairman UPGB.pdf"},
    {"name": "Circular 3 - Establishment of UPGB", "file": "Circular No. 03 dated 01.05.2025.pdf"},
    {"name": "Circular 4 - Interest rates on SBA and TD", "file": "Circular No. 04 dated 01.05.2025.pdf"},
    {"name": "Circular 5 - Loan Policy", "file": "Circular No 5 Loan Policy 2025-26.pdf"},
    {"name": "Circular 6 - Third Party Tie-up", "file": "Cir_06 तृतीय पक्ष बीमा व्यवसाय हेतु कॉर्पोरेट टाई-अप कंपनियों द्वारा बीमा कराने के संबंध म.pdf"},
    {"name": "Circular 7 - Loan Schemes", "file": "Circular No 7 Loan Schemes_compressed.pdf"},
    {"name": "Circular 8 - Advance service charges", "file": "Circular no 8 Service Charges.pdf"},
    {"name": "Circular 9 - ROI Advances", "file": "Circular no 9 ROI.pdf"},
    {"name": "Circular 10 - DLP of credit hub", "file": "Circular No 10 DLP of Credit Hub and RLF.pdf"},
    {"name": "Circular 11 - Service Charges", "file": "Cir No 11 Service Charges for Uttar Pradesh Gramin Bank.pdf"},
    {"name": "Circular 12 - Recovery Policy", "file": "Cir No.12_Recovery Policy with annex.pdf"},
    {"name": "Circular 13 - Staff Accountability", "file": "Cir No.13_Policy on Staff Accountability with annexure.pdf"},
    {"name": "Circular 14 - Master Direction on Counterfeit Notes", "file": "Cir. No. 14 Dated-01.05.2025 Master Direction on Counterfeit Notes, 2025.pdf"},
    {"name": "Circular 15 - Liability Product", "file": "Cir No-15_Liability Product.pdf"},
    {"name": "Circular 16 - Risk Based Internal Audit Policy", "file": "Cir-16 Risk Based Internal Audit Policy_compressed.pdf"},
    {"name": "Circular 17 - Concurrent Audit Policy", "file": "Cir-17 Concurrent Audit Policy_compressed.pdf"},
    {"name": "Circular 18 - Revenue Audit Policy", "file": "Cir-18 Revenue Audit Policy.pdf"},
    {"name": "Circular 19 - Snap Audit Policy", "file": "Cir-19 Snap Audit Policy.pdf"},
    {"name": "Circular 20 - Special Audit Policy", "file": "Cir-20 Special Audit Policy.pdf"},
    {"name": "Circular 21 - Information System Audit Policy", "file": "Cir-21 Information System Audit Policy (Version-1.o)_compressed.pdf"},
    {"name": "Circular 22 - Management Audit Policy", "file": "Cir-22 Management Audit Policy.pdf"},
    {"name": "Circular 23 - Revised Discretionary Administrative Powers", "file": "Circulaer 23 Revised Descretionary Administrative Powers for Domestic Operations.pdf"},
    {"name": "Circular 24 - Commision to BCs", "file": "Cir.No. 24_Commission Payable to Business Correspondents (BCs)_01.05.2025.pdf"},
    {"name": "Circular 25 - RIDER CLAUSE", "file": "CIRCULAR 25 DT 29.04.2025 RIDER CLAUSE.pdf"}
]

# Extract text from a PDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pdf_text += page.get_text()
    return pdf_text

# API endpoint to get the list of PDFs
@app.route("/api/circulars", methods=["GET"])
def get_pdfs():
    return jsonify(pdfs)

# API endpoint to search PDFs by content
@app.route("/api/search", methods=["GET"])
def search_pdfs():
    query = request.args.get("query", "").lower()
    results = []

    # Searching the content of each PDF
    for pdf in pdfs:
        pdf_path = os.path.join(PDFS_DIRECTORY, pdf["file"])
        pdf_text = extract_text_from_pdf(pdf_path)
        
        # If the query is found inside the PDF text
        if query in pdf_text.lower():  # Simple case-insensitive search
            results.append(pdf)

    return jsonify(results)

# Serve PDF files (static files)
@app.route("/api/pdf/<filename>")
def serve_pdf(filename):
    pdf_path = os.path.join(PDFS_DIRECTORY, filename)
    if os.path.exists(pdf_path):
        return send_from_directory(PDFS_DIRECTORY, filename)
    return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
