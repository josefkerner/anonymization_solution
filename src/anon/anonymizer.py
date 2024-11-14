
import re
import unidecode
from src.language.language_detector import LinguaLanguageDetector
from anonymization import (Anonymization, AnonymizerChain,
                           PhoneNumberAnonymizer,
                           EmailAnonymizer, NamedEntitiesAnonymizer)
class Anonymizer:
    def __init__(self):

        self.language_detector = LinguaLanguageDetector()


    def anonymize(self, text: str) -> str:
        lang, conf = self.language_detector.detect_with_confidence(
            text=text
        )
        print(lang, conf)
        if lang == 'cs':
            lang = 'cs_CZ'
            ner_model = 'en_core_web_lg'
        elif lang == 'de':
            lang = 'de_DE'
            ner_model = 'de_core_news_lg'
        elif lang == 'en':
            lang = 'en_US'
            ner_model = 'en_core_web_lg'
        else:
            raise ValueError(f"Unsupported language: {lang}")

        #remove diacritics
        #text = unidecode.unidecode(text)
        #replace every number in text with 'X'
        text = ''.join(['0' if c.isdigit() else c for c in text])

        #replace websites
        url_regex = 'www\.[a-zA-Z0-9]+\.[a-zA-Z]+'
        text = re.sub(url_regex,'wwww.website.com',text)

        #replace every company name followed by 'a.s' with 'COMPANY a.s.'
        #company name can contain diacritics such as Česká spořitelna a.s.
        pattern = r'([áéíóúůýžčřďťňÁÉÍÓÚŮÝŽČŘĎŤŇ]|[a-z]|[A-Z])+ a\.s\.'
        text = re.sub(pattern, 'COMPANY', text)

        #replace every company name followed by 's.r.o' with 'COMPANY s.r.o.'
        text = re.sub(r'([áéíóúůýžčřďťňÁÉÍÓÚŮÝŽČŘĎŤŇ]|[a-z]|[A-Z])+ s\.r\.o\.', 'COMPANY s.r.o.', text)

        #replace every company name followed by 'gmbh' with 'COMPANY s.r.o.'
        text = re.sub(r'([A-Z][a-z]+ )+gmbh', 'COMPANY gmbh', text)




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
