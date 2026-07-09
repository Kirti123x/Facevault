import numpy as np


class FaceMatcher:

    def cosine_similarity(
        self,
        embedding1,
        embedding2
    ):

        embedding1 = np.asarray(
            embedding1,
            dtype=np.float32
        )

        embedding2 = np.asarray(
            embedding2,
            dtype=np.float32
        )

        embedding1 = embedding1 / np.linalg.norm(
            embedding1
        )

        embedding2 = embedding2 / np.linalg.norm(
            embedding2
        )

        similarity = np.dot(
            embedding1,
            embedding2
        )

        return float(similarity)

    def compare(
        self,
        embedding1,
        embedding2,
        threshold=0.60
    ):

        similarity = self.cosine_similarity(
            embedding1,
            embedding2
        )

        return similarity >= threshold

    def distance(
        self,
        embedding1,
        embedding2
    ):

        similarity = self.cosine_similarity(
            embedding1,
            embedding2
        )

        return 1.0 - similarity