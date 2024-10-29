import os
from src.extraction_service.extraction_service import ExtractionService
#from src.extraction_service.pdf.pdf_ocr_service import PdfOcrService
from pdfminer.high_level import extract_text
import base64
from datetime import datetime
class PdfExtraction(ExtractionService):

    def __init__(self):
        pass
        #self.ocr = PdfOcrService()

    def extract_file(self, filename:str) -> str:
        text = extract_text(filename)
        ocr_used = False
        print(f"length of text is {len(text)}")
        if len(text) < 100:
            pass
            #self.ocr.ocr(filename)
            #text = self.extract_file(f"OCR_{filename}")
            #ocr_used = True
        # remove file after extraction
        #if ocr_used: os.remove(f"OCR_{filename}")
        return text

    def extract_text(self,file:str) -> str:
        '''
        :param file
        '''
        try:
            dt = datetime.now()
            dt = str(dt).replace(' ','_').replace(':','_').replace('.','_')
            file = base64.b64decode(file)
            name = f"example_{dt}.pdf"
            f = open(name,'wb')
            f.write(file)
            f.close()
            text = self.extract_file(name)

            return text

        except Exception as e:
            raise ValueError(f"Error extracting text from pdf: {e}")

