import io
from src.extraction_service.extraction_service import ExtractionService
import os
from docx import Document
import base64

class WordExtractionService(ExtractionService):
    def extract_text(self, file: str, base_path :str = os.getcwd()) -> str:


        file = base64.b64decode(file)

        filename = f'{base_path}\\report.docx'
        f = open(filename, 'wb')
        f.write(file)
        print(f'File saved: {filename}')
        f.close()

        return self.extract_file(filename)


    def extract_file(self, filename: str):
        doc = Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)

        #os.remove(filename)
        return '\n'.join(fullText)


