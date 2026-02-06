import cv2
import numpy as np
import os
from keras_facenet import FaceNet

# --- FaceNet and Face Detector Setup ---
# The keras_facenet library automatically downloads the pre-trained model.
embedder = FaceNet()

# Pre-trained OpenCV DNN face detector for robust face detection.
face_detector_dnn = cv2.dnn.readNetFromCaffe(
    'data/deploy.prototxt', 
    'data/res10_300x300_ssd_iter_140000.caffemodel'
)
# ---------------------------------------

video = cv2.VideoCapture(0)
faces_embeddings = []
names_list = []

i = 0
name = os.getenv("PERSON_NAME") or input("Enter Name: ")

print("Collecting face embeddings. Please look at the camera...")

while True:
    ret, frame = video.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_detector_dnn.setInput(blob)
    detections = face_detector_dnn.forward()

    for k in range(detections.shape[2]):
        confidence = detections[0, 0, k, 2]

        if confidence > 0.5:
            box = detections[0, 0, k, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            crop_img = frame[startY:endY, startX:endX, :]
            
            if crop_img.size > 0:
                # FaceNet requires a 160x160 RGB image.
                resized_img = cv2.resize(crop_img, (160, 160))
                
                if len(faces_embeddings) <= 100 and i % 5 == 0:
                    # Get the embedding for the cropped face using FaceNet.
                    embedding = embedder.embeddings(np.expand_dims(resized_img, axis=0))[0]
                    faces_embeddings.append(embedding)
                    names_list.append(name)
                
                i += 1
                cv2.putText(frame, str(len(faces_embeddings)), (startX, startY - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
    
    cv2.imshow("Face Embedding Collection", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_embeddings) >= 100:
        break

video.release()
cv2.destroyAllWindows()

# Convert to numpy arrays.
faces_embeddings = np.asarray(faces_embeddings)
names_list = np.asarray(names_list)

# Save embeddings and names using numpy.
if not os.path.exists('data/'):
    os.makedirs('data/')

if 'faces_embeddings.npz' in os.listdir('data/'):
    with np.load('data/faces_embeddings.npz') as data:
        existing_embeddings = data['embeddings']
        existing_names = data['names']
    
    combined_embeddings = np.append(existing_embeddings, faces_embeddings, axis=0)
    combined_names = np.append(existing_names, names_list, axis=0)
    
    np.savez_compressed('data/faces_embeddings.npz', embeddings=combined_embeddings, names=combined_names)
else:
    np.savez_compressed('data/faces_embeddings.npz', embeddings=faces_embeddings, names=names_list)

print("Face embeddings and names saved successfully using NumPy.")