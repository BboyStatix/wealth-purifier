import os
import sys
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(module_path)

from flask import Flask, request, jsonify
from services import ExtractInterestService

app = Flask(__name__)

@app.route('/report/generate', methods=['POST'])
def generate_interest_report():
  statement_type = request.form.get('statementType')
  statements = request.files.getlist('files')
  print("Calculating Interest...")
  interestEntries = ExtractInterestService.extract_interest(statement_type, statements)
  totalInterest = sum([entry[1] for entry in interestEntries])
  print(f"Total Interest: {totalInterest}")
  return jsonify(interestEntries)
