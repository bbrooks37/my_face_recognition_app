# Import necessary libraries for database connection, environment variables, and array handling.
import os
import sys
import psycopg2
import numpy as np
from dotenv import load_dotenv

# Load environment variables from the .env file.
# This ensures that sensitive information like the database URI is not hardcoded.
load_dotenv()

# The name of the file whose face you want to search for in the database.
# This file must have its embedding already calculated and stored in the database.
# You can change this to any of your detected face files (e.g., 'bb_face_0.jpg' or 'jb_face_0.jpg').
SEARCH_FILE_NAME = "pb_face_0.jpg"

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

def find_most_similar_face(conn, embedding_to_search):
    """
    Finds the most similar face in the database to a given embedding.

    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        embedding_to_search (numpy.ndarray): The embedding of the face to search for.

    Returns:
        tuple or None: A tuple containing the file name and the distance of the most
                       similar face, or None if no match is found.
    """
    try:
        with conn.cursor() as cur:
            # The numpy array needs to be converted to a simple string of floats for pgvector.
            # We explicitly convert each element to a string and join them with commas.
            embedding_str = '[' + ','.join([str(x) for x in embedding_to_search]) + ']'
            
            # The '<=>' operator calculates the L2 distance between the embeddings.
            # We order by distance to find the closest match (the smallest distance).
            # We limit to 1 result and also exclude the search file itself from the results.
            cur.execute("""
                SELECT picture, embedding <=> %s AS distance
                FROM pictures
                WHERE picture != %s
                ORDER BY distance
                LIMIT 1
            """, (embedding_str, SEARCH_FILE_NAME))
            
            result = cur.fetchone()
            return result

    except Exception as e:
        print(f"Error finding most similar face: {e}")
        return None

def main():
    """
    Main function to run the face search application.
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

        # Retrieve the embedding for the search file.
        search_embedding = get_embedding_from_db(conn, SEARCH_FILE_NAME)
        if search_embedding is None:
            print(f"Could not find an embedding for '{SEARCH_FILE_NAME}'.")
            return

        # Find the most similar face in the database.
        most_similar = find_most_similar_face(conn, search_embedding)
        
        if most_similar:
            file_name, distance = most_similar
            print(f"The face in '{SEARCH_FILE_NAME}' is most similar to the face in '{file_name}'.")
            print(f"Similarity Score (L2 Distance): {distance}")
        else:
            print("No similar faces found in the database.")

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
