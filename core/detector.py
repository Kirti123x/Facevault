import cv2
from insightface.app import FaceAnalysis


class FaceDetector:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l"
        )

        self.app.prepare(
            ctx_id=-1,
            det_size=(640, 640)
        )

    def detect(self, image_path):

        img = cv2.imread(image_path)

        if img is None:
            return []

        faces = self.app.get(img)

        boxes = []

        for face in faces:

            x1, y1, x2, y2 = face.bbox.astype(int)

            boxes.append([
                x1,
                y1,
                x2,
                y2
            ])

        return boxes