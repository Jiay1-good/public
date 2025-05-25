from flask import Flask, request, jsonify
import os
from flask_cors import CORS
# Import actual models
from recommendation import PersonalizedDietRecommendation

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend cross-domain requests

# Configure file paths using relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Starting server for frontend-backend connection")

@app.route('/api/recommend-diet', methods=['POST'])
def recommend_diet():
    try:
        # Get user data
        data = request.json
        if not data:
            return jsonify({"error": "No user data provided"}), 400
        
        # Validate required fields
        required_fields = ['height', 'weight', 'age', 'gender', 'activityLevel']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Try to use actual recommendation system
        try:
            recommender = PersonalizedDietRecommendation(
                height=float(data['height']),
                weight=float(data['weight']),
                age=int(data['age']),
                gender=data['gender'],
                activity_level=data['activityLevel']
            )
            recommendation, macros = recommender.recommend()
            
            # Return only the diet recommendation
            return jsonify(recommendation)
        except Exception as e:
            return jsonify({"error": f"Error generating diet recommendation: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible externally
    app.run(debug=True, host='0.0.0.0', port=5001)
