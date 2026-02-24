import logging
import os

def configure_logging(service_name: str | None = None):
    level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO) # optional

    logging.basicConfig(
          #      ! set the default level to INFO
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        force=True,
    )

    # silence thirdparty libraries
    for library in ("pymongo", "PIL", "pytesseract"):
        logging.getLogger(library).setLevel(logging.WARNING)
