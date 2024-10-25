import base64
from src.extraction_service.extraction_service import ExtractionService
class TextGenerationService(ExtractionService):
    def extract_text(self, file: str) -> str:
        '''
        Will extract text from provided bytes based on service type
        :param file:
        :return:
        '''
        txt = base64.b64decode(file)
        return txt.decode('utf-8')
