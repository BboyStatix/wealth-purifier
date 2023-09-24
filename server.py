from flask import Flask, request, send_from_directory, jsonify
from services import ExtractInterestService

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return send_from_directory('.', 'index.html')

@app.route('/report/generate', methods=['POST'])
def generate_interest_report():
  statement_type = request.form.get('statementType')
  statements = request.files.getlist('files')
  print("Calculating Interest...")
  interestEntries = ExtractInterestService.extract_interest(statement_type, statements)
  totalInterest = sum([entry[1] for entry in interestEntries])
  print(f"Total Interest: {totalInterest}")
  return jsonify(interestEntries=interestEntries, total=totalInterest)

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)