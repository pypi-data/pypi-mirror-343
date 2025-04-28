"""
Ukrainian Passport recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrPassportRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian Passport (Паспорт зразка 1994 року): 
    two letters followed by six digits.
    """
    PATTERNS = [
        # Basic format: 2 Ukrainian letters + 6 digits
        Pattern(
            name="passport_basic", 
            regex=r"\b[А-ЯІЇЄҐ]{2}\d{6}\b", 
            score=0.1
        ),
        # With prefix "серія" or "паспорт"
        Pattern(
            name="passport_with_prefix", 
            regex=r"\b(?:паспорт серії)[:\s]*[А-ЯІЇЄҐ]{2}\d{6}\b", 
            score=1.0
        ),
    ]

    CONTEXT = [
        "паспорт",
        "серія",
        "виданий",
        "РВ УМВС",
        "РО УМВД"
    ]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_PASSPORT",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="ukr_passport_recognizer",
            supported_language="uk"
        )