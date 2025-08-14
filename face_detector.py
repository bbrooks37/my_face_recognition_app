# Import the required libraries.
import os
import cv2

# List of image files you want to process.
# You can add more files to this list as needed.
image_files = ['bb.jpg', 'jb.jpg', 'pb.jpg', 'rb.jpg', 'cw.jpg', 'cw2.jpg']

# Directory to save the detected faces.
output_dir = 'detected_faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the pre-trained Haar Cascade classifier for face detection.
# Make sure the XML file is in the same directory as your script.
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default (1).xml'
)

def detect_and_save_faces(image_path, output_directory, image_filename):
    """
    Detects faces in an image and saves each face as a separate file.
    
    Args:
        image_path (str): The path to the input image.
        output_directory (str): The directory to save the output files.
        image_filename (str): The original filename of the image.
    """
    try:
        # Read the image.
        img = cv2.imread(image_path)
        
        # Convert the image to grayscale, which is required for the Haar Cascade classifier.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image.
        # `scaleFactor` and `minNeighbors` are parameters that you can adjust
        # to improve detection accuracy.
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3, # Lowered to be less strict
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Iterate over the detected faces and save each one.
        for i, (x, y, w, h) in enumerate(faces):
            # Crop the detected face from the original image.
            face_img = img[y:y+h, x:x+w]
            
            # Create a new filename for the cropped face.
            base_filename = os.path.splitext(image_filename)[0]
            output_filename = f"{base_filename}_face_{i}.jpg"
            output_path = os.path.join(output_directory, output_filename)
            
            # Save the cropped face image.
            cv2.imwrite(output_path, face_img)
        
        print(f"Detected and saved {len(faces)} face(s) from '{image_filename}'.")
        return len(faces)
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return 0

def main():
    """
    Main function to run face detection on a list of images.
    """
    total_faces_saved = 0
    # Process each image file in the list.
    for file in image_files:
        faces_saved = detect_and_save_faces(file, output_dir, file)
        total_faces_saved += faces_saved
    
    print(f"\nCompleted face detection. A total of {total_faces_saved} face(s) were saved.")

if __name__ == "__main__":
    main()

