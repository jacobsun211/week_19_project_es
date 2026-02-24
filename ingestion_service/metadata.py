import os
import uuid
from PIL import Image
# pip install pillow

class ImageData:
    def __init__(self, image_id, imageName, file_size_bytes, width, height, file_format, path):
        self.image_id = image_id
        self.imageName = imageName
        self.file_size_bytes = file_size_bytes
        self.width = width
        self.height = height
        self.file_format = file_format
        self.path = path
        self.text = None

class MetadataExtractor:
    def extract_metadata(self, folder: str) -> list:
        results = []
        for image in os.listdir(folder):
            path = os.path.join(folder, image) # creating the full image path, folder path + image name
            try:
                with Image.open(path) as img:
                    image_obj = ImageData(
                        image_id=str(uuid.uuid4()),
                        imageName=image,
                        file_size_bytes=os.path.getsize(path),
                        width=img.width,
                        height=img.height,
                        file_format=img.format,
                        path=path
                    )
                    results.append(image_obj)
            except Exception:
                pass  # skip non image files
        return results
