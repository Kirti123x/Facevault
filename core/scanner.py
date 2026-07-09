import os

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff"
}


def scan_images(folder_path):
    """
    Recursively scan a folder and return all image paths.
    """

    images = []

    if not os.path.exists(folder_path):
        return images

    for root, _, files in os.walk(folder_path):

        for file in files:

            # Ignore hidden files
            if file.startswith("."):
                continue

            extension = os.path.splitext(file)[1].lower()

            if extension in IMAGE_EXTENSIONS:

                full_path = os.path.join(root, file)

                if os.path.isfile(full_path):
                    images.append(full_path)

    images.sort()
    return images