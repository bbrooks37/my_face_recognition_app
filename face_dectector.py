# Import the OpenCV library, which is commonly aliased as cv2.
import cv2
import os

# The name of the XML file containing the pre-trained Haar Cascade classifier.
alg = "haarcascade_frontalface_default (1).xml"

# Load the Haar Cascade algorithm from the XML file into OpenCV.
haar_cascade = cv2.CascadeClassifier(alg)

# The name of the image file you want to analyze.
file_name = 'bb.jpg'

# Read the image as a grayscale image.
img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

# Check if the image was loaded successfully.
if img is None:
    print(f"Error: Could not load image file '{file_name}'. Please check the file path.")
else:
    # Find the faces in the image.
    faces = haar_cascade.detectMultiScale(
        img,
        scaleFactor=1.05,
        minNeighbors=2,
        minSize=(100, 100)
    )

    # A counter to keep track of the number of faces detected.
    face_count = 0

    # Define the output directory and create it if it doesn't exist.
    output_dir = 'detected_faces'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # For each face detected, a new cropped image will be saved.
    for x, y, w, h in faces:
        # Crop the image to select only the face.
        cropped_image = img[y:y + h, x:x + w]

        # Define the name of the file where the cropped image will be stored.
        target_file_name = f'detected_face_{face_count}.jpg'

        # Create the full path for the new image file.
        target_file_path = os.path.join(output_dir, target_file_name)

        # Write the cropped image to the 'detected_faces' folder.
        cv2.imwrite(
            target_file_path,
            cropped_image,
        )

        # Increment the face counter.
        face_count += 1

    if face_count > 0:
        print(f"Detected and saved {face_count} face(s) to the '{output_dir}' folder.")
    else:
        print(f"No faces detected in '{file_name}'.")

