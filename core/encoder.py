import cv2
from insightface.app import FaceAnalysis


class FaceEncoder:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l"
        )

        self.app.prepare(
            ctx_id=-1,
            det_size=(640, 640)
        )

    def encode(self, image_path):

        img = cv2.imread(image_path)

        if img is None:
            return []

        faces = self.app.get(img)

        embeddings = []

        for face in faces:
            embeddings.append(face.embedding)

        return embeddings