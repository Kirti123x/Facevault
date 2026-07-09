import os
import cv2
import numpy as np
from sklearn.cluster import DBSCAN

from core.scanner import scan_images
from core.detector import FaceDetector
from core.encoder import FaceEncoder
from core.database import Database
from core.thumbnail import create_thumbnail


class FaceIndexer:
    def __init__(self):
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.database = Database()

    def index_folder(
        self,
        folder_path,
        progress_callback=None
    ):

        images = scan_images(folder_path)

        total = len(images)

        if total == 0:
            return

        database_faces = []

        # -----------------------------
        # Step 1 : Collect all faces
        # -----------------------------

        for index, image_path in enumerate(images):

            print("Processing:", image_path)

            img = cv2.imread(image_path)

            if img is None:
                continue

            faces = self.detector.detect(image_path)

            if len(faces) == 0:
                continue

            encodings = self.encoder.encode(image_path)

            for face, encoding in zip(faces, encodings):
                x1, y1, x2, y2 = map(int, face)

                # Keep coordinates inside image
                h, w = img.shape[:2]

                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)

                crop = img[y1:y2, x1:x2]

                if crop.size == 0:
                    continue

                database_faces.append({

                    "image": image_path,
                    "embedding": encoding,
                    "thumbnail": crop

                })

            if progress_callback:
                progress_callback(
                    int(((index + 1) / total) * 50)
                )

        if len(database_faces) == 0:
            return

        # -----------------------------
        # Step 2 : Cluster all faces
        # -----------------------------

        embeddings = np.array(
            [f["embedding"] for f in database_faces],
            dtype=np.float32
        )

        embeddings = embeddings / np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True
        )

        clustering = DBSCAN(
            eps=0.42,
            min_samples=1,
            metric="cosine"
        )

        labels = clustering.fit_predict(embeddings)

       # -----------------------------
        # Step 3 : Save clustered people
        # -----------------------------

        person_map = {}

        total_faces = len(database_faces)

        for i, (label, face) in enumerate(zip(labels, database_faces)):

            if label not in person_map:

                person_name = f"Person_{label + 1}"

                person_id = self.database.add_person(
                    person_name
                )

                person_map[label] = person_id

            person_id = person_map[label]

            photo_id = self.database.add_photo(
                face["image"]
            )

            try:

                thumb_path = create_thumbnail(
                    face["thumbnail"],
                    person_id,
                    photo_id
                )

            except Exception as e:

                print("Thumbnail Error:", e)

                thumb_path = None

            self.database.add_face(
                photo_id,
                person_id,
                face["embedding"],
                thumb_path
            )

            if progress_callback:

                progress_callback(
                    50 + int(((i + 1) / total_faces) * 50)
                )

        print(
            f"Finished indexing {len(database_faces)} faces."
        )