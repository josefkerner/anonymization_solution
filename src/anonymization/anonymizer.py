from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from src.language.language_detector import LinguaLanguageDetector
from anonymization import (Anonymization, AnonymizerChain,
                           PhoneNumberAnonymizer,
                           EmailAnonymizer, NamedEntitiesAnonymizer)
class Anonymizer:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.language_detector = LinguaLanguageDetector()


    def anonymize(self, text: str) -> str:
        lang, conf = self.language_detector.detect_with_confidence(
            text=text
        )
        print(lang, conf)
        if lang == 'cs':
            lang = 'cs_CZ'
            ner_model = 'en_core_web_lg'


        elif lang == 'en':
            lang = 'en_US'
            ner_model = 'en_core_web_lg'
        #exit(1)
        self.anon = AnonymizerChain(Anonymization(lang))
        self.anon.add_anonymizers(EmailAnonymizer,
                                  NamedEntitiesAnonymizer(ner_model),
                                  PhoneNumberAnonymizer
                                  )
        text = self.anon.anonymize(text)
        '''
        analyzer_results = self.analyzer.analyze(text=text, language=lang)
        result = self.anonymizer.anonymize(
            text=text, analyzer_results=analyzer_results
        )
        '''

        return text
