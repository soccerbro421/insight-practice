import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

class FaceComparer:
    def __init__(self):
        self.model = FaceAnalysis()
        self.model.prepare(ctx_id=0, det_size=(640, 640))

    def get_faces(self, img_file):
        img = cv2.imread(img_file)
        faces = self.model.get(img)
        return faces[0] if len(faces) > 0 else None

    def calculate_similarity(self, normalized_embedding1, normalized_embedding2):
        reshaped_embedding1 = normalized_embedding1.reshape(1, -1)
        reshaped_embedding2 = normalized_embedding2.reshape(1, -1)
        similarity_score = cosine_similarity(reshaped_embedding1, reshaped_embedding2)
        percentage_similarity = similarity_score[0][0] * 100
        print(f"The faces are {percentage_similarity}% similar.")

    def compare_faces(self, img_file1, img_file2):
        face1 = self.get_faces(img_file1)
        face2 = self.get_faces(img_file2)

        if face1 is not None and face2 is not None:
            norm_embed1 = face1.normed_embedding
            norm_embed2 = face2.normed_embedding
            self.calculate_similarity(norm_embed1, norm_embed2)
        else:
            print("Could not detect a face in one or both of the images.")


file1 = "./images/joji1.png"
file2 = "./images/joji2.png"

face_comparer = FaceComparer()
face_comparer.compare_faces(file1, file2)
