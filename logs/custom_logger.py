import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_dir = os.path.join(project_root, "log_dir")
        os.makedirs(self.log_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
        log_file_path = os.path.join(self.log_dir, log_file)

        logging.basicConfig(
            filename=log_file_path,
            format="[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d) : %(message)s",
            level=logging.INFO,
        )

    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))
