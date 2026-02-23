# PROJECT TREE

```
.env
analytics/ [subfolders: 0, files: 2, total files: 2]
    Dockerfile
    requirements.txt
cleaning_consumer/ [subfolders: 0, files: 2, total files: 2]
    Dockerfile
    requirements.txt
docker-compose.yaml
elastic_consumer/ [subfolders: 0, files: 2, total files: 2]
    Dockerfile
    requirements.txt
GridFS Service/ [subfolders: 0, files: 1, total files: 1]
    requirements.txt
ingestion_service/ [subfolders: 3, files: 5, total files: 13]
    __pycache__/ [subfolders: 0, files: 3, total files: 3]
        image.cpython-313.pyc
        main.cpython-313.pyc
        text_extractor.cpython-313.pyc
    connection/ [subfolders: 1, files: 2, total files: 4]
        __pycache__/ [subfolders: 0, files: 2, total files: 2]
            kafka.cpython-313.pyc
            mongo.cpython-313.pyc
        kafka.py
        mongo.py
    init.py
    main.py
    metadata.py
    requirements.txt
    send/ [subfolders: 0, files: 1, total files: 1]
        send_to_kafka.py
    text_extractor.py
```

# PROJECT STATS

- Total folders: 9
- Total files  : 22

## File types

| Extension | Files | Lines (utf-8 text only) |
|---|---:|---:|
| `.py` | 7 | 142 |
| `.pyc` | 5 | 0 |
| `.txt` | 5 | 14 |
| `.yaml` | 1 | 153 |
| `no_ext` | 4 | 1 |

---

# FILE CONTENTS

## .env

```
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
```

## GridFS Service/requirements.txt

```

```

## analytics/Dockerfile

```

```

## analytics/requirements.txt

```

```

## cleaning_consumer/Dockerfile

```

```

## cleaning_consumer/requirements.txt

```

```

## docker-compose.yaml

```yaml

services:
# +--------------------+
# |       MONGO        |
# +--------------------+
  mongo:
    image: mongo:7
    restart: unless-stopped
    ports:
      - "27017:27017" # TODO: change if port 27017 is already used
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: app # TODO:: set per project
      MONGO_INITDB_ROOT_PASSWORD: app_pw # TODO:: set per project
      MONGO_INITDB_DATABASE: suspicious # TODO:: set per project
    networks:
      - es


# +--------------------+
# |   MONGO UI (WEB)   |
# +--------------------+
  mongo-express:
    image: mongo-express:1.0.2
    restart: unless-stopped
    ports:
      - "18081:8081" # TODO: change if port 8081 is already used
    environment:
      ME_CONFIG_MONGODB_URL: "mongodb://app:app_pw@mongo:27017/?authSource=admin" # TODO: keep in sync with mongo creds
      ME_CONFIG_BASICAUTH: "false"
    depends_on:
      - mongo
    networks:
      - es



# +--------------------+
# |       KAFKA        |
# +--------------------+
  kafka:
    image: confluentinc/cp-kafka:7.6.1
    restart: unless-stopped
    ports:
      - "9092:9092" # TODO: change if port 9092 is already used
    environment:
      CLUSTER_ID: "Mf_-9PUJQnCI6eQZzgFTlg" # TODO: set per project
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka:9093"

      # listeners
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092" # TODO: if you change host port 9092, update this
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT,CONTROLLER:PLAINTEXT"
      KAFKA_INTER_BROKER_LISTENER_NAME: "PLAINTEXT"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"

      # single node dev defaults
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    networks:
      - es

# +--------------------+
# |      KAFKA UI      |
# +--------------------+
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    restart: unless-stopped
    ports:
      - "18080:8080" # TODO: change if port 8080 is already used
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: "kafka:29092"
    depends_on:
      - kafka
    networks:
      - es


# +--------------------+
# |   Elasticsearch    |
# +--------------------+
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    volumes:
      - esdata:/usr/share/elasticsearch/data

# +--------------------+
# |   Kibana           |
# +--------------------+
  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  esdata:
  mongo_data:

networks:
  es:
    driver: bridge

# elastic_consumer:
#     build:
#       context: .
#       dockerfile: elastic_consumer/Dockerfile
#     restart: unless-stopped
#     depends_on:
#       - kafka
#     networks:
#       - es


# cleaning_consumer:
#   build:
#     context: .
#     dockerfile: cleaning_consumer/Dockerfile
#   restart: unless-stopped
#   depends_on:
#     - kafka
#   networks:
#     - es



# analytics:
#   build:
#     context: .
#     dockerfile: analytics/Dockerfile
#   restart: unless-stopped
#   depends_on:
#     - kafka
#   networks:
#     - es
```

## elastic_consumer/Dockerfile

```

```

## elastic_consumer/requirements.txt

```

```

## ingestion_service/__pycache__/image.cpython-313.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service/__pycache__/main.cpython-313.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service/__pycache__/text_extractor.cpython-313.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service/connection/__pycache__/kafka.cpython-313.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service/connection/__pycache__/mongo.cpython-313.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service/connection/kafka.py

```python
import os
from confluent_kafka import Producer



SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


producer = Producer({"bootstrap.servers": SERVER})
```

## ingestion_service/connection/mongo.py

```python
import os
from pymongo import MongoClient




host = os.getenv("MONGO_HOST", "localhost")
port = int(os.getenv("MONGO_PORT", "27017"))

MONGO_USER = os.getenv("MONGO_USER","app")          # e.g. "app"
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "app_pw")      # e.g. "app_pw"
MONGO_AUTHSOURCE = os.getenv("MONGO_AUTHSOURCE", "admin")  # root user auth DB is typically admin [page:2]
MONGO_DB = os.getenv("MONGO_DB", "pizza")

client = MongoClient(
    host,
    port,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource=MONGO_AUTHSOURCE,
)
```

## ingestion_service/init.py

```python

```

## ingestion_service/main.py

```python
from fastapi import FastAPI
from connection.kafka import producer
from connection.mongo import client
from metadata import extract_metadata
from text_extractor import get_clean_text
from send.send_to_kafka import kafka_send

db = client["week19"]
collection = db["images"]

app = FastAPI()

path = 'data\\messaging_images\\tweet_images'

# @app.get("/uploadfile")
# def get_file():
#     print('yo')
#     images = extract_metadata(path)
#     with_text =  get_clean_text(images)
#     return with_text

# @app.get("to_grid") # TODO: send to mongo
# def post_to_grid():
#     print("gotcha")
#     images = extract_metadata(path) # get the metadata
#     images = get_clean_text(images) # add the text
#     return kafka_send(images)

    
@app.post("/send_to_kafka")
def get_file():
    
    print("gotcha")
    images = extract_metadata(path) # get the metadata
    images = get_clean_text(images) # add the text
    return kafka_send(images)









# uvicorn main:app --reload



    

```

## ingestion_service/metadata.py

```python
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

```

## ingestion_service/requirements.txt

```
confluent-kafka==2.13.0
dnspython==2.8.0
fastapi==0.131.0
h11==0.16.0
idna==3.11
ImageIO==2.37.2
numpy==2.4.2
packaging==26.0
pillow==12.1.1
pydantic==2.12.5
pydantic_core==2.41.5
pymongo==4.16.0
pytesseract==0.3.13
uvicorn==0.41.0
```

## ingestion_service/send/send_to_kafka.py

```python
from connection.kafka import producer
import json

WRITING_TOPIC = "RAW"


def kafka_send(images):
    for image in images:
        image = json.dumps(image).encode('utf-8')
        producer.produce("RAW", image)
        producer.poll(0)  

    return {"count": len(images)}
```

## ingestion_service/text_extractor.py

```python
from PIL import Image
import pytesseract
# pip install pytesseract


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def get_clean_text(images):
    full_images = []
    for image in images:
        raw_image = Image.open(image["path"])
        # gray_image = raw_image.convert("L") # improving visibility for reading the text

        text = pytesseract.image_to_string(raw_image) # getting the text

        image["text"] = text
        full_images.append(image)
    return full_images

```

