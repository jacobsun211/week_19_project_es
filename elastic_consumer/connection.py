from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


es = Elasticsearch('http://localhost:9200')


result = es.ping()
print('Connected:', result)




index_name = "images_test"

def health_check():
    exists = es.indices.exists(index=index_name) # check if the index exists
    print(f"Exists before delete: {exists}")

    # Step 2: If it exists, delete it.
    if exists:
        es.indices.delete(index=index_name)
        print(f"Deleted index '{index_name}'")


mapping = {
    "properties": {
        "image_id":       {"type": "keyword"},
        "imageName":      {"type": "keyword"},
        "file_size_bytes":{"type": "integer"},
        "width":          {"type": "integer"},
        "height":         {"type": "integer"},
        "file_format":    {"type": "keyword"},
        "text":           {"type": "text"},
        "raw_text":       {"type": "text"}
    }
}

class ImageData:
    def __init__(self, image_id, imageName, file_size_bytes, width, height, file_format, path, text):
        self.image_id = image_id
        self.imageName = imageName
        self.file_size_bytes = file_size_bytes
        self.width = width
        self.height = height
        self.file_format = file_format
        self.path = path
        self.text = text
        self.raw_text = None

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings=mapping)
    print(f"Created index '{index_name}' with mapping.")

# Step 4: Confirm it exists again. Print True.
exists_after = es.indices.exists(index=index_name)
print(f"Exists after create: {exists_after}")



def insert(image):
    response = es.index( # insert, or update if exist
        index="images_test",      
        id=image.image_id,        
        document=image.__dict__
    )

