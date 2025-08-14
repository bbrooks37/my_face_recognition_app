# Import the necessary libraries.
import os
import sys
import psycopg2
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from imgbeddings import imgbeddings
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Get the database URI from the environment variables.
SERVICE_URI = os.getenv('SERVICE_URI')

# Initialize the Flask application. We will use a templates folder to serve the HTML.
app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests from your front-end.

def get_embedding_from_image(image_file):
    """
    Calculates the embedding for a face in a given image file.

    Args:
        image_file: The file object of the uploaded image.

    Returns:
        list: The embedding as a flattened list of floats, or None if an error occurs.
    """
    try:
        # Load the image using PIL from the file stream.
        image = Image.open(BytesIO(image_file.read()))
        
        # Initialize the imgbeddings model.
        ibed = imgbeddings()

        # Calculate the 768-dimensional embedding.
        embedding = ibed.to_embeddings(image)
        
        # Flatten the NumPy array and convert it to a list.
        return embedding.flatten().tolist()
    except Exception as e:
        print(f"Error calculating embedding: {e}", file=sys.stderr)
        return None

def calculate_l2_distance(embedding1, embedding2):
    """
    Calculates the L2 distance between two embeddings.

    Args:
        embedding1 (list): The first embedding.
        embedding2 (list): The second embedding.

    Returns:
        float: The L2 distance (Euclidean distance).
    """
    try:
        # Convert the lists back to NumPy arrays for calculation.
        arr1 = np.array(embedding1)
        arr2 = np.array(embedding2)

        # Normalize the embeddings. This is a crucial step for accurate distance comparison.
        arr1_norm = arr1 / np.linalg.norm(arr1)
        arr2_norm = arr2 / np.linalg.norm(arr2)

        # Calculate the L2 distance.
        distance = np.linalg.norm(arr1_norm - arr2_norm)
        return float(distance)
    except Exception as e:
        print(f"Error calculating distance: {e}", file=sys.stderr)
        return None

@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():
    """
    API endpoint to compare two face images and return a similarity score.
    """
    # Check if the request contains the required files.
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Please upload two images."}), 400

    image1_file = request.files['image1']
    image2_file = request.files['image2']

    # Get the embeddings for both images.
    embedding1 = get_embedding_from_image(image1_file)
    embedding2 = get_embedding_from_image(image2_file)

    if embedding1 is None or embedding2 is None:
        return jsonify({"error": "Could not process one or both images. Ensure a single face is visible."}), 500

    # Calculate the L2 distance (similarity score).
    distance = calculate_l2_distance(embedding1, embedding2)
    
    if distance is None:
        return jsonify({"error": "An error occurred during distance calculation."}), 500

    # Return the similarity score as a JSON object.
    return jsonify({"score": distance})

@app.route('/')
def home():
    """
    Serves the index.html file from the templates folder.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Run the application. The host is set to '0.0.0.0' to make it accessible
    # from outside the container in a typical development setup.
    app.run(host='0.0.0.0', port=5000)
