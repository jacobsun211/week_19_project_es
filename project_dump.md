# PROJECT TREE

```
.env
analytics/ [subfolders: 0, files: 1, total files: 1]
    Dockerfile
chat.py
cleaning_consumer/ [subfolders: 0, files: 3, total files: 3]
    Dockerfile
    main.py
    models.py
docker-compose.yaml
elastic_consumer/ [subfolders: 0, files: 1, total files: 1]
    Dockerfile
ingestion_service/ [subfolders: 3, files: 4, total files: 12]
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
    send/ [subfolders: 0, files: 1, total files: 1]
        send_to_kafka.py
    text_extractor.py
project_dump.md
```

# PROJECT STATS

- Total folders: 8
- Total files  : 21

## File types

| Extension | Files | Lines (utf-8 text only) |
|---|---:|---:|
| `.md` | 1 | 0 |
| `.py` | 10 | 529 |
| `.pyc` | 5 | 0 |
| `.yaml` | 1 | 153 |
| `no_ext` | 4 | 37 |

---

# FILE CONTENTS

## .env

```
# ── Kafka (shared) ─────────────────────────────────────
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# ── MongoDB ────────────────────────────────────────────
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=app
MONGO_PASSWORD=app_pw
MONGO_AUTHSOURCE=admin
MONGO_DB=suspicious

# ── Ingestion Service ──────────────────────────────────
INGESTION_WRITING_TOPIC=RAW

# ── Cleaning Consumer ──────────────────────────────────
CLEANING_LISTENING_TOPIC=RAW
CLEANING_WRITING_TOPIC=clean

# ── Analytics ──────────────────────────────────────────
ANALYTICS_LISTENING_TOPIC=clean
ANALYTICS_WRITING_TOPIC=analytics



# ── Elastic Consumer ───────────────────────────────────
ELASTIC_CONSUMER_LISTENING_TOPIC1=RAW
ELASTIC_CONSUMER_LISTENING_TOPIC2=clean
ELASTIC_CONSUMER_LISTENING_TOPIC3=analytics

ELASTICSEARCH_HOST=http://elasticsearch
ELASTICSEARCH_PORT=9200

# ---- other -----
LOG_LEVEL=INFO
LOG_SILENCE=pymongo,PIL,pytesseract

```

## analytics/Dockerfile

```

```

## chat.py

```python
"""
project_overview.py
Utility -> universal structure + full content dump script

Default behavior:
- Includes only git-tracked files (git ls-files)
- Writes output to project_dump.md
- Skips selected folders + ignore files (see EXCLUDED_* below)

Optional:
- Include ignored + untracked files listed by git (can be huge!)
"""
from __future__ import annotations
import argparse
import os
from collections import defaultdict
from pathlib import Path
import subprocess
from typing import Dict, Any, List, TextIO, Tuple
                               
# -----------------------------
# EXCLUDES (customize here)
# -----------------------------
EXCLUDED_DIR_NAMES = {
    "venv",
    ".venv",   # common; remove if not desired
    "general",
    "arc",
    "ignore",
    "data",
    
}

EXCLUDED_FILE_NAMES = {
    ".gitignore",
    ".dockerignore",
    "requirements.txt",
    "chat"
}


def is_excluded_path(file_path: str) -> bool:
    """
    Returns True if file_path should be excluded based on directory/file name rules.
    - Excludes if any path segment matches EXCLUDED_DIR_NAMES
    - Excludes if the file name matches EXCLUDED_FILE_NAMES
    """
    p = Path(file_path)

    # Exclude specific filenames anywhere
    if p.name in EXCLUDED_FILE_NAMES:
        return True

    # Exclude any file inside excluded directories (at any depth)
    if any(part in EXCLUDED_DIR_NAMES for part in p.parts):
        return True

    return False


# -----------------------------
# GIT FILE LISTING
# -----------------------------
def get_git_files(include_ignored: bool) -> List[str]:
    """
    Returns file paths relative to repo root.
    include_ignored=False:
      - tracked files only
    include_ignored=True:
      - tracked + untracked + ignored (gitignored)

    Then filters out excluded paths (venv/general/arc/ignore dirs + .gitignore/.dockerignore files).
    """
    if include_ignored:
        cmd = ["git", "ls-files", "--cached", "--others", "--ignored", "--exclude-standard"]
    else:
        cmd = ["git", "ls-files"]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Git command failed. Are you in a git repository?\n"
            f"Command: {' '.join(cmd)}\n"
            f"Error: {result.stderr.strip()}"
        )

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Apply exclusions
    files = [fp for fp in files if not is_excluded_path(fp)]
    return files


# -----------------------------
# TREE BUILDING
# -----------------------------
Tree = Dict[str, Any]  # nested dict; leaf files are None


def add_to_tree(tree: Tree, file_path: str) -> None:
    parts = Path(file_path).parts
    current = tree
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = None


def sum_files(node: Tree) -> int:
    count = 0
    for v in node.values():
        if isinstance(v, dict):
            count += sum_files(v)
        else:
            count += 1
    return count


def count_folders(node: Tree) -> int:
    """
    Counts folders recursively (each dict node is a folder).
    """
    total = 0
    for v in node.values():
        if isinstance(v, dict):
            total += 1
            total += count_folders(v)
    return total


def print_tree(node: Tree, out: TextIO, prefix: str = "") -> None:
    for key, value in sorted(node.items(), key=lambda kv: kv[0].lower()):
        if isinstance(value, dict):
            subfolders = sum(1 for v in value.values() if isinstance(v, dict))
            files = sum(1 for v in value.values() if v is None)
            total_files = sum_files(value)
            out.write(
                f"{prefix}{key}/ [subfolders: {subfolders}, files: {files}, total files: {total_files}]\n"
            )
            print_tree(value, out, prefix + "    ")
        else:
            out.write(f"{prefix}{key}\n")


# -----------------------------
# CONTENT DUMP HELPERS
# -----------------------------
def is_probably_binary(path: str, sniff_bytes: int = 2048) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(sniff_bytes)
        if b"\x00" in chunk:
            return True
        # If it decodes as UTF-8, assume text
        try:
            chunk.decode("utf-8")
            return False
        except UnicodeDecodeError:
            return True
    except Exception:
        # If we can't read it, treat as "not text dumpable"
        return True


def language_from_extension(ext: str) -> str:
    ext = ext.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "jsx",
        ".tsx": "tsx",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".md": "markdown",
        ".html": "html",
        ".css": "css",
        ".sh": "bash",
        ".bat": "bat",
        ".ps1": "powershell",
        ".java": "java",
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".rs": "rust",
        ".go": "go",
        ".sql": "sql",
        ".xml": "xml",
        ".ini": "ini",
        ".env": "",
    }.get(ext, "")


def safe_read_text(path: str, max_bytes: int) -> Tuple[str | None, str | None]:
    """
    Returns (text, error). If too large/binary/unreadable, text is None and error explains why.
    """
    try:
        size = os.path.getsize(path)
        if size > max_bytes:
            return None, f"SKIPPED (too large: {size} bytes > limit {max_bytes} bytes)"
        if is_probably_binary(path):
            return None, "SKIPPED (binary or non-UTF8 text)"
        with open(path, "r", encoding="utf-8", errors="strict") as f:
            return f.read(), None
    except UnicodeDecodeError:
        return None, "SKIPPED (not UTF-8 decodable)"
    except Exception as e:
        return None, f"SKIPPED (read error: {e})"


# -----------------------------
# MAIN
# -----------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Project overview + full code dump to a single file.")
    parser.add_argument("--out", default="project_dump.md", help="Output file path (default: project_dump.md)")
    parser.add_argument(
        "--include-ignored",
        action="store_true",
        help="Include gitignored + untracked files (can be huge). Default is tracked files only.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=1_000_000,
        help="Max file size to include in content dump (default: 1,000,000 bytes).",
    )
    args = parser.parse_args()

    all_files = get_git_files(include_ignored=args.include_ignored)

    tree: Tree = {}
    file_types = defaultdict(int)
    file_lines = defaultdict(int)

    # Build tree + stats
    for file_path in all_files:
        add_to_tree(tree, file_path)
        ext = Path(file_path).suffix or "no_ext"
        file_types[ext] += 1

        # Count lines only for readable utf-8 text files within size limit
        text, err = safe_read_text(file_path, max_bytes=args.max_bytes)
        if text is not None:
            file_lines[ext] += text.count("\n") + (1 if text else 0)

    total_files = len(all_files)
    total_folders = count_folders(tree)

    out_path = Path(args.out)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("# PROJECT TREE\n\n")
        out.write("```\n")
        print_tree(tree, out)
        out.write("```\n\n")

        out.write("# PROJECT STATS\n\n")
        out.write(f"- Total folders: {total_folders}\n")
        out.write(f"- Total files  : {total_files}\n\n")

        out.write("## File types\n\n")
        out.write("| Extension | Files | Lines (utf-8 text only) |\n")
        out.write("|---|---:|---:|\n")
        for ext, count in sorted(file_types.items(), key=lambda kv: kv[0].lower()):
            out.write(f"| `{ext}` | {count} | {file_lines[ext]} |\n")
        out.write("\n---\n\n")

        out.write("# FILE CONTENTS\n\n")
        for file_path in all_files:
            out.write(f"## {file_path}\n\n")
            text, err = safe_read_text(file_path, max_bytes=args.max_bytes)
            if text is None:
                out.write(f"**{err}**\n\n")
                continue
            lang = language_from_extension(Path(file_path).suffix)
            out.write(f"```{lang}\n")
            out.write(text)
            if not text.endswith("\n"):
                out.write("\n")
            out.write("```\n\n")

    print(f"Wrote project dump to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
```

## cleaning_consumer/Dockerfile

```

```

## cleaning_consumer/main.py

```python
from confluent_kafka import Consumer, Producer
from cleaning_consumer.models import ImageData
import json
import os
from confluent_kafka import Producer
import logging
from shared.logging_config import configure_logging
configure_logging("cleaning_consumer.main")                                               
#                              ! the name of the file -> 2026-02-24 10:08:41,733 [INFO] __main__ - Sent image 'tweet_9.png' to topic 'clean'
# logger = logging.getLogger(__name__)                                                  !!!!!!!!  
logger = logging.getLogger("cleaning_consumer.main")



SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = Producer({"bootstrap.servers": SERVER})





WRITING_TOPIC = os.getenv("CLEANING_WRITING_TOPIC", "clean")
LISTENS_TOPIC = os.getenv("CLEANING_LISTENING_TOPIC", "RAW")


conf = {
    'bootstrap.servers': SERVER,
    'group.id': "cleaning consumer",
    'auto.offset.reset': 'earliest'
}



consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])

def send_to_kafka(image: ImageData):
        imageName = image.imageName
        #                           ! since its a class object, we need to convert it to dict and THEN to str
        image = json.dumps(image.__dict__).encode('utf-8')
        producer.produce(WRITING_TOPIC, image)
        logger.info(f"Sent image '{imageName}' to topic '{WRITING_TOPIC}'")
        producer.poll(0)



def clean():
    while True:
            image = consumer.poll(1.0) 
            if image is None: continue
            if image.error():
                print(f"cleaner error: {image.error()}")
                continue


            image = json.loads(image.value()) # from str to dict
            image = ImageData(**image) # from dict to class object
            image.text = image.text.replace("\x0c", "").replace("?", "").replace("!", "").strip().lower() # cleaning the text
            send_to_kafka(image)
         
clean()

# python -m cleaning_consumer.main
```

## cleaning_consumer/models.py

```python
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


class KafkaConnection:
    def __init__(self):
        SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = Producer({"bootstrap.servers": SERVER})


producer = KafkaConnection().producer
```

## ingestion_service/connection/mongo.py

```python
import os
from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", "27017"))

        MONGO_USER = os.getenv("MONGO_USER","app")          # e.g. "app"
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "app_pw")      # e.g. "app_pw"
        MONGO_AUTHSOURCE = os.getenv("MONGO_AUTHSOURCE", "admin")  # root user auth DB is typically admin [page:2]
        MONGO_DB = os.getenv("MONGO_DB", "pizza")

        self.client = MongoClient(
            host,
            port,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            authSource=MONGO_AUTHSOURCE,
        )


client = MongoConnection().client
```

## ingestion_service/init.py

```python

```

## ingestion_service/main.py

```python
from fastapi import FastAPI
import logging
from .connection.mongo import client
from .metadata import MetadataExtractor
from .text_extractor import TextExtractor
from .send.send_to_kafka import KafkaSender
from shared.logging_config import configure_logging

configure_logging("ingestion_service")



logging.getLogger("ingestion_service.kafka_sender")
logger = logging.getLogger(__name__)


db = client["week19"]
collection = db["images"]

app = FastAPI()

path = 'data\\messaging_images\\tweet_images'

metadata = MetadataExtractor()
text = TextExtractor()
kafka = KafkaSender()

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
    images = metadata.extract_metadata(path) # get the metadata
    for image in images:
        image_with_text = text.get_clean_text(image) # add the text
        kafka.send(image_with_text)
    return {"count": len(images)}


    
# from week_19_project_es/
# uvicorn ingestion_service.main:app --reload
```

## ingestion_service/metadata.py

```python
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
```

## ingestion_service/send/send_to_kafka.py

```python
from ..connection.kafka import producer
import os
import json
import logging
logger = logging.getLogger(__name__)


WRITING_TOPIC = os.getenv("INGESTION_WRITING_TOPIC", "RAW")


class KafkaSender:
    def send(self, image):
        try:#                            ! must when working with classes
            payload = json.dumps(image.__dict__).encode("utf-8")
            producer.produce(WRITING_TOPIC, payload)
            producer.poll(0)
            logger.info(f"Sent image '{image.imageName}' to topic '{WRITING_TOPIC}'")
        except Exception as e:
            raise
```

## ingestion_service/text_extractor.py

```python
from PIL import Image
import pytesseract
# pip install pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class TextExtractor:
    def get_clean_text(self, image):
        raw_image = Image.open(image.path)

        # gray_image = raw_image.convert("L") # improving visibility for reading the text
        text = pytesseract.image_to_string(raw_image) # getting the text
        image.text = text
        return image
```

## project_dump.md

**SKIPPED (binary or non-UTF8 text)**

