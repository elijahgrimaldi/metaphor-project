from flask import Flask, jsonify, request
from flask_cors import CORS
from analyze_stock import analyze_stock

app = Flask(__name__)
CORS(app)

@app.route('/stock_analysis', methods=['POST'])
def execute_script():
    try:
        # Get data from the React frontend
        data = request.json
        symbol = data.get('symbol')
        if not symbol:
            return jsonify({"error": "Symbol not provided"}), 400
        
        # Execute your script here and get the result
        result_data = analyze_stock(symbol)
        
        # Check that the result_data is in the expected format
        if "overall_sentiment" not in result_data or "sentiment_counts" not in result_data:
            return jsonify({"error": "Invalid response format from analyze_stock"}), 500

        return jsonify({"result": result_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
