# Import necessary libraries for database connection, environment variables, and array handling.
import os
import sys
import psycopg2
import numpy as np
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Define the two files you want to compare.
# You can change these to any two file names you have in your database.
FILE_NAME_1 = "cw_face_0.jpg"
FILE_NAME_2 = "jb_face_0.jpg"

def get_embedding_from_db(conn, file_name):
    """
    Retrieves the embedding for a given file from the database.
    
    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        file_name (str): The name of the file to search for.
    
    Returns:
        numpy.ndarray or None: The face embedding as a numpy array if found, otherwise None.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT embedding FROM pictures WHERE picture = %s", (file_name,))
            result = cur.fetchone()
            if result:
                # The embedding is a text representation of a PostgreSQL array.
                # It needs to be converted into a numpy array for processing.
                embedding_str = result[0].replace('{', '[').replace('}', ']')
                return np.array(eval(embedding_str))
            else:
                return None
    except Exception as e:
        print(f"Error retrieving embedding for '{file_name}': {e}")
        return None

def main():
    """
    Main function to calculate and print the L2 distance between two face embeddings.
    """
    # Get the database URI from the environment variables.
    service_uri = os.getenv("SERVICE_URI")
    if not service_uri:
        print("Error: SERVICE_URI not found in environment variables.")
        sys.exit(1)

    conn = None
    try:
        # Connect to the PostgreSQL database.
        conn = psycopg2.connect(service_uri)
        print("Successfully connected to the database!")

        # Retrieve the embeddings for both files.
        embedding1 = get_embedding_from_db(conn, FILE_NAME_1)
        embedding2 = get_embedding_from_db(conn, FILE_NAME_2)

        if embedding1 is None or embedding2 is None:
            print(f"Could not find embeddings for one or both files: '{FILE_NAME_1}' or '{FILE_NAME_2}'.")
            return

        # Normalize the embeddings. This is crucial for getting meaningful L2 distances
        # that are comparable across different searches.
        embedding1_norm = embedding1 / np.linalg.norm(embedding1)
        embedding2_norm = embedding2 / np.linalg.norm(embedding2)

        # Calculate the L2 distance between the normalized embeddings.
        distance = np.linalg.norm(embedding1_norm - embedding2_norm)

        print(f"The L2 Distance between '{FILE_NAME_1}' and '{FILE_NAME_2}' is:")
        print(f"Similarity Score (L2 Distance): {distance}")

    except psycopg2.Error as e:
        print(f"A database connection error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
