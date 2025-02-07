from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load responses from the JSON file
with open('responses.json', 'r') as f:
    data = json.load(f)

# Preprocess the responses
inputs = [item['input'] for item in data]
responses = [item['response'] for item in data]

# Initialize the TF-IDF Vectorizer and transform the input text data
vectorizer = TfidfVectorizer().fit(inputs)
input_vectors = vectorizer.transform(inputs)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')  # Get the message from the frontend
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Find the most similar response
    ai_response = get_response(user_message)
    return jsonify({"response": ai_response})

def get_response(user_message):
    # Convert the user input to a vector
    user_vector = vectorizer.transform([user_message])
    
    # Calculate cosine similarity between user input and predefined responses
    similarities = cosine_similarity(user_vector, input_vectors)
    
    # Find the index of the response with the highest similarity
    best_match_index = similarities.argmax()
    return responses[best_match_index]

if __name__ == '__main__':
    app.run(debug=True)
