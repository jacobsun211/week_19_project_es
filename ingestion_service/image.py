import os
import uuid
from PIL import Image
# pip install pillow

def extract_metadata(folder: str) -> list[dict]:
    results = []
    for image in os.listdir(folder):
        path = os.path.join(folder, image) # creating the full image path, folder path + image name
        try:
            with Image.open(path) as img:
                results.append({
                    "image_id":        str(uuid.uuid4()),
                    "imageName":        image,
                    "file_size_bytes": os.path.getsize(path),
                    "width":           img.width,
                    "height":          img.height,
                    "file_format":     img.format,
                    "path":            path
            
                })
        except Exception:
            pass  # skip non image files
    return results

