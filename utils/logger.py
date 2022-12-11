import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

class Logger:
    def __init__(self, name: str, level: int = logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def getInstance(self):
        return self.logger