import json

from utils.logger import Logger

class JsonReader:
    logger = Logger(__name__).getInstance()

    @staticmethod
    def load(fileName: str) -> dict:
        data = {}
        
        try:
            with open(fileName) as f:
                data = json.load(f)
        except:
            JsonReader.logger.error("JsonReader.load. Error opening file and get data")
            
        return data