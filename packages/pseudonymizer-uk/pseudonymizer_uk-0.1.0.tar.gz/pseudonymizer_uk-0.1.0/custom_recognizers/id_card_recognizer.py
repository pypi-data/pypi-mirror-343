"""
Ukrainian ID Card recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrIdCardRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian ID Card (ID-картка): 
    nine digits, with optional prefix.
    """
    PATTERNS = [
        # Basic format: 9 digits
        Pattern(
            name="id_card_basic", 
            regex=r"\b\d{9}\b", 
            score=0.1
        ),
        # With prefix "ID-картка" or "електронний паспорт"
        Pattern(
            name="id_card_with_prefix", 
            regex=r"\b(?:ID-картка|паспорт номер|паспорт №|паспорт)[:\s]*\d{9}\b", 
            score=1.0
        ),
    ]

    CONTEXT = [
        "ID-картка",
        "паспорт номер",
        "паспорт №",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_ID_CARD",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="ukr_id_card_recognizer",
            supported_language="uk"
        ) 