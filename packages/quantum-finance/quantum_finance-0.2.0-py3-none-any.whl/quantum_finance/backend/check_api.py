from flask import Flask, request, jsonify

# Create a Flask app instance
app = Flask(__name__)

# Add some test routes with the same names as in api.py
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'version': '1.0.0'})

@app.route('/api/query', methods=['POST'])
def handle_query():
    return jsonify({'response': 'Test response'})

@app.route('/api/random', methods=['GET'])
def handle_random():
    return jsonify({'response': 'Random response'})

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    return jsonify(['query1', 'query2', 'query3'])

if __name__ == '__main__':
    print('Available routes:')
    for rule in app.url_map.iter_rules():
        print(f'  {rule.endpoint} -> {rule.rule}')
        
    # Run the app if executed directly
    app.run(debug=True, port=5002) 