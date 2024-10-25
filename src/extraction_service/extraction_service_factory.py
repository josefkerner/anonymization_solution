from src.extraction_service.word.word_extraction import WordExtractionService
from src.extraction_service.pdf.pdf_extraction import PdfExtraction
from src.extraction_service.web.web_extraction_service import WebExtractionService
from src.extraction_service.txt.txt_extraction import TextGenerationService
from src.extraction_service.extraction_service import ExtractionService
from src.extraction_service.rtf.rtf_service import RtfService
from src.data_models.file_input import Input

class ExtractionServiceFactory:
    def __init__(self):
        word_service = WordExtractionService()
        self.services = {
            'pdf': PdfExtraction(),
            'word': word_service,
            'docx': word_service,
            'doc': word_service,
            'web': WebExtractionService(),
            'txt': TextGenerationService(),
            'rtf': RtfService()
        }
    def get_extraction_service(self, input: Input) -> ExtractionService:
        '''

        :param input:
        :return:
        '''
        if input.type in self.services:
            return self.services[input.type]
        else:
            raise NotImplementedError(f"Wrong input type {input.type}")


