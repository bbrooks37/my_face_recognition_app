# Import the OpenCV library, which is commonly aliased as cv2.
import cv2
import os

# The name of the XML file containing the pre-trained Haar Cascade classifier.
# Note: The file name has been updated to match the one you provided in the image.
alg = "haarcascade_frontalface_default (1).xml"

# Load the Haar Cascade algorithm from the XML file into OpenCV.
# This classifier is a machine learning model that detects objects (in this case, faces).
haar_cascade = cv2.CascadeClassifier(alg)

# List of all the images you want to process.
image_files = ['bb.jpg', 'jb.jpg', 'pb.jpg']

# A counter to keep track of the number of faces detected.
total_face_count = 0

# For each image file in the list, process it to find faces.
for file_name in image_files:
    # Read the image as a grayscale image.
    # Grayscale images are often used for object detection as they simplify the data.
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded successfully.
    if img is None:
        print(f"Error: Could not load image file '{file_name}'. Please check the file path.")
        continue

    # Find the faces in the image.
    # This function returns an array of face locations and sizes.
    # The parameters control the detection sensitivity and size of faces to be detected.
    faces = haar_cascade.detectMultiScale(
        img,
        scaleFactor=1.05,
        minNeighbors=2,
        minSize=(100, 100)
    )

    # For each face detected, a new cropped image will be saved.
    # The loop iterates over all detected faces.
    for i, (x, y, w, h) in enumerate(faces):
        # Crop the image to select only the face using the coordinates (x, y) and dimensions (w, h).
        cropped_image = img[y:y + h, x:x + w]

        # Define the name of the file where the cropped image will be stored.
        # This now includes the original filename to make the output files more descriptive.
        base_name, _ = os.path.splitext(file_name)
        target_file_name = f'{base_name}_face_{i}.jpg'

        # Write the cropped image to a file.
        cv2.imwrite(
            target_file_name,
            cropped_image,
        )

        total_face_count += 1
    
    # Print a confirmation message once the process is complete for each image.
    if len(faces) > 0:
        print(f"Detected and saved {len(faces)} face(s) from '{file_name}'.")
    else:
        print(f"No faces detected in '{file_name}'.")

print(f"\nCompleted face detection. A total of {total_face_count} face(s) were saved.")
