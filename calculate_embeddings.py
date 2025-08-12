import os
import glob
import psycopg2
from imgbeddings import imgbeddings
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your Aiven PostgreSQL connection string is now an environment variable
SERVICE_URI = os.getenv('SERVICE_URI')

# Function to get embeddings for all detected faces
def get_image_embeddings(images_folder="detected_faces"):
    image_paths = glob.glob(os.path.join(images_folder, "*.jpg"))
    print(f"Found {len(image_paths)} images in '{images_folder}'.")

    if not image_paths:
        print("No images found. Please check the 'detected_faces' folder.")
        return {}

    embeddings_dict = {}
    print("Calculating embeddings...")
    ibed = imgbeddings()

    for image_path in image_paths:
        try:
            pil_image = Image.open(image_path)
            embedding = ibed.to_embeddings(pil_image)
            # Flatten the NumPy array before converting it to a list
            embeddings_dict[os.path.basename(image_path)] = embedding.flatten().tolist()
            print(f"Calculated embedding for {os.path.basename(image_path)}")
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
    return embeddings_dict

# Main function to connect to PostgreSQL and save embeddings
def main():
    if not SERVICE_URI:
        print("Error: SERVICE_URI not found. Please check your .env file.")
        return

    print("Starting to calculate embeddings for detected faces...")
    embeddings = get_image_embeddings()

    if not embeddings:
        print("No embeddings to save. Exiting.")
        return

    print("Embedding calculation complete. Connecting to PostgreSQL...")

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(SERVICE_URI)
        cur = conn.cursor()
        print("Successfully connected to the database!")

        cur.execute("CREATE TABLE IF NOT EXISTS pictures (picture VARCHAR(255), embedding vector(768));")
        conn.commit()
        print("Table 'pictures' checked/created successfully.")
        
        print("Saving embeddings to the database...")
        for filename, embedding in embeddings.items():
            cur.execute("INSERT INTO pictures (picture, embedding) VALUES (%s, %s)", (filename, embedding))
            print(f"Saved embedding for {filename}")
        
        conn.commit() # Commit all insertions at once
        print("All embeddings have been saved and committed to the database.")
        
        # Verify the number of rows inserted
        cur.execute("SELECT COUNT(*) FROM pictures;")
        row_count = cur.fetchone()[0]
        print(f"Successfully inserted {len(embeddings)} row(s). Total rows in table: {row_count}")

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
