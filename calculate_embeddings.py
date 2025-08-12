# First, you need to install the required packages. You can run these commands
# in your terminal before running this script.
# pip install imgbeddings
# pip install pillow
# pip install numpy
# pip install psycopg2
# pip install python-dotenv

# Import the required libraries.
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import os
import sys
import psycopg2
from dotenv import load_dotenv

# The directory where your image files are located.
# In this case, it's the current directory.
image_directory = '.'

# A counter to keep track of the number of embeddings calculated.
embedding_count = 0

# A list to store the embeddings and filenames.
embeddings_to_save = []

# Iterate over all files in the directory to find the detected faces.
print("Starting to calculate embeddings for detected faces...")

for filename in os.listdir(image_directory):
    # We are looking for files that end with '_face_0.jpg' as saved by the face-detector.
    if filename.endswith('_face_0.jpg'):
        try:
            # Load the face image from its file.
            file_path = os.path.join(image_directory, filename)
            img = Image.open(file_path)

            # Load the `imgbeddings` model so we can calculate embeddings.
            # This is done inside the loop to ensure it's re-initialized if needed.
            ibed = imgbeddings()
            
            # Calculate the 768-dimensional embedding for the image.
            # The result is a NumPy array.
            embedding = ibed.to_embeddings(img)[0]

            # Store the filename and embedding in our list.
            embeddings_to_save.append((filename, embedding))

            # Print the filename and the resulting embedding for verification.
            print(f"\n--- Embedding for '{filename}' ---")
            print("---")
            embedding_count += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"\nEmbedding calculation complete. Processed {embedding_count} image(s).")

# Now, connect to the PostgreSQL database and store the embeddings.
print("Connecting to PostgreSQL and saving embeddings...")

# Load environment variables from the .env file.
# The `dotenv_path` argument can be used to specify the path to the .env file if it's not in the current directory.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Get the database URI from the environment variables.
service_uri = os.getenv("SERVICE_URI")

if not service_uri:
    print("Error: SERVICE_URI not found in environment variables.")
    # Exit the script if the URI is not found.
    sys.exit(1)
else:
    print("SERVICE_URI loaded successfully.")
    
conn = None
try:
    # Connect to the database.
    conn = psycopg2.connect(service_uri)
    cur = conn.cursor()

    # Loop through the list of calculated embeddings and insert or update them in the table.
    for filename, embedding in embeddings_to_save:
        # The embedding must be converted to a list for psycopg2 to handle it correctly.
        # We use an ON CONFLICT clause to either insert a new row or update the existing one.
        cur.execute(
            'INSERT INTO pictures (picture, embedding) VALUES (%s, %s) ON CONFLICT (picture) DO UPDATE SET embedding = EXCLUDED.embedding',
            (filename, embedding.tolist())
        )
        print(f"Successfully inserted/updated embedding for '{filename}'.")

    # Commit the transaction to save the changes.
    conn.commit()
    print("All embeddings have been saved to the database.")

except psycopg2.Error as e:
    # Handle any errors that occur during the database operation.
    print(f"Database error: {e}")

finally:
    # Close the cursor and the connection to the database.
    if 'cur' in locals() and cur:
        cur.close()
    if conn:
        conn.close()
    print("Database connection closed.")
