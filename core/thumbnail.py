import os
import cv2

THUMBNAIL_SIZE = (200, 200)


def create_thumbnail(face_crop, person_id, photo_id):

    folder = os.path.join(
        "thumbnails",
        str(person_id)
    )

    os.makedirs(folder, exist_ok=True)

    thumbnail = cv2.resize(
        face_crop,
        THUMBNAIL_SIZE
    )

    output_path = os.path.join(
        folder,
        f"{photo_id}.jpg"
    )

    cv2.imwrite(
        output_path,
        thumbnail
    )

    return output_path