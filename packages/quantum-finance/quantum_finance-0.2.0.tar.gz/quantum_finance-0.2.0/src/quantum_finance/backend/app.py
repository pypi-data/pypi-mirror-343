from flask import Flask, request, jsonify
from src.quantum_finance.backend.ml_framework import MLFramework
from src.quantum_finance.backend.port_manager import PortManager
from src.quantum_finance.backend.app_insights import setup_insights_for_flask_app

app = Flask(__name__)
ml_framework = MLFramework()

# Set up insights middleware to track errors and performance
insights = setup_insights_for_flask_app(app)

# Use insights_route instead of app.route for automatic performance tracking
@app.route('/predict', methods=['POST'])
@insights.insights_route(endpoint='/predict')
def predict():
    json_data = request.get_json(silent=True) or {}
    if 'data' not in json_data:
        return jsonify({'error': 'Missing "data" field'}), 400

    data = json_data['data']
    prediction = ml_framework.predict(data)
    return jsonify({'prediction': prediction})

@app.route('/feedback', methods=['POST'])
@insights.insights_route(endpoint='/feedback')
def feedback():
    json_data = request.get_json(silent=True) or {}
    if 'prediction' not in json_data or 'isPositive' not in json_data:
        return jsonify({'error': 'Missing required fields'}), 400

    prediction = json_data['prediction']
    is_positive = json_data['isPositive']
    ml_framework.update_model_with_feedback(prediction, is_positive)
    return jsonify({'status': 'success'})

# Add an endpoint to get insights about the application
@app.route('/admin/insights', methods=['GET'])
def get_insights():
    # Only allow access from localhost for security
    if request.remote_addr not in ['127.0.0.1', 'localhost']:
        return jsonify({'error': 'Access denied'}), 403
        
    health = insights.tracker.analyze_project_health()
    api_recommendations = insights.get_recommended_api_improvements()
    
    return jsonify({
        'health': health,
        'api_recommendations': api_recommendations
    })

if __name__ == '__main__':
    # Use the port manager to avoid conflicts
    port_mgr = PortManager()
    
    # Try to get the port from environment variable, or use a default
    import os
    preferred_port = int(os.environ.get('PORT', 5002))
    
    # Get an available port, preferring the one specified
    port = port_mgr.get_available_port(preferred_port)
    
    # Register this component's port usage
    port_mgr.register_port_usage("flask_backend", port)
    
    print(f"Starting Flask backend on port {port}")
    app.run(debug=True, port=port)