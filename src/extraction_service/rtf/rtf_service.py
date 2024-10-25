
from src.extraction_service.extraction_service import ExtractionService
from langchain_community.document_loaders import UnstructuredRTFLoader
import base64



class RtfService(ExtractionService):
    def __init__(self):
        pass

    def extract_text(self, file: str) -> str:
        '''
        Will extract text from provided bytes based on service type
        :param file:
        :return:
        '''
        #decode the base64 file to bytes
        base64_bytes = base64.b64decode(file)
        #save the file to the disk
        with open("example.rtf", "wb") as f:
            f.write(base64_bytes)

        loader = UnstructuredRTFLoader(
        'example.rtf', mode ='elements', strategy ='fast'

        )
        total_docs = []
        docs = loader.load()
        for doc in docs:
            total_docs.append(doc.page_content)

        if len(docs) == 0:
            res = "No text found in the document"
        else:
            res = ' '.join(total_docs)


        return res