import os
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

#import fasttext
from lingua import Language, LanguageDetectorBuilder



# Suppress FastText warning about load_model API change
#fasttext.FastText.eprint = lambda x: None


class LanguageDetector(ABC):
    """Base class for language detection."""

    def __init__(self, languages: Optional[List[str]] = None) -> None:
        self.languages = languages

        self.load_model()

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def detect(self, text: str) -> str:
        pass

    @abstractmethod
    def detect_with_confidence(self, text: str) -> Tuple[str, float]:
        pass





class LinguaLanguageDetector(LanguageDetector):
    """Detect the language of text snippets using Lingua."""

    def __init__(self, languages: Optional[List[str]] = None) -> None:
        super().__init__(languages=languages)

    def load_model(self) -> None:
        if self.languages:
            lingua_languages = self.load_languages(self.languages)
            self._detector = LanguageDetectorBuilder.from_languages(*lingua_languages).build()
        else:
            self._detector = LanguageDetectorBuilder.from_all_languages().build()

    def load_languages(self, languages: List[str]) -> List[Language]:
        try:
            return [Language[language.upper()] for language in languages]
        except KeyError:
            supported_languages = {language.name.lower() for language in Language}
            not_supported_languages = set(languages) - supported_languages
            raise ValueError(f"Found unsupported languages: {', '.join(not_supported_languages)}")

    def detect(self, text: str) -> str:
        """Detect language of text and return language ISO code."""
        language = self._detector.detect_language_of(text)
        return language.iso_code_639_1.name.lower()

    def detect_with_confidence(self, text: str, num_digits: int = 4) -> Tuple[str, float]:
        """Detect language of text and return language ISO code and probability."""
        predictions = self._detector.compute_language_confidence_values(text)
        try:
            language, language_prob = predictions[0].language, predictions[0].value
            language_code = language.iso_code_639_1.name.lower()
        except IndexError:
            language_code, language_prob = "", 0.0

        return language_code, round(language_prob, num_digits)
