from abc import ABC, abstractmethod
class ExtractionService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract_text(self, file: str) -> str:
        '''
        Will extract text from provided bytes based on service type
        :param file:
        :return:
        '''
        pass