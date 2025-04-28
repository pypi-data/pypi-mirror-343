"""
Ukrainian ЄДРПОУ recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrEdrpouRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian ЄДРПОУ: eight digits, 
    with optional prefix.
    """
    PATTERNS = [
        # bare 8 digits
        Pattern(name="eight_digits", regex=r"\b\d{8}\b", score=0.5),
        # prefixed forms: ЄДРПОУ 12345678 (colon optional)
        Pattern(
            name="ukr_edrpou_prefixed", 
            regex=r"\b(?:ЄДРПОУ|Єдиний державний реєстр підприємств та організацій України)[:\s]*\d{8}\b", 
            score=1.0
        ),
    ]

    CONTEXT = [
        "ЄДРПОУ",
        "Єдиний державний реєстр",
        "підприємств",
        "організацій",
        "України",
        "реєстр",
        "реєстрація",
        "облік",
        "юридична особа",
        "фізична особа",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_EDRPOU",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="ukr_edrpou_recognizer",
            supported_language="uk"
        ) 