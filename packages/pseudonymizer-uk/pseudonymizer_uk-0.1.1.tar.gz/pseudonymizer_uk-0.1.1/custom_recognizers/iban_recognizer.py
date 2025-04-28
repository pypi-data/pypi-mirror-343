"""
Ukrainian IBAN recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrIbanRecognizer(PatternRecognizer):
    """
    Dedicated recognizer for Ukrainian IBAN (UAkk 6n 19n), 
    without invoking full SWIFT registry.
    """
    PATTERNS = [
        Pattern(
            name="ua_iban_compact",
            regex=r"\bUA\d{2}\d{6}\d{19}\b",
            score=1.0,
        ),
        Pattern(
            name="ua_iban_spaced",
            regex=r"\bUA(?:\s?\d{2})(?:\s?\d{6})(?:\s?\d{19})\b",
            score=1.0,
        ),
    ]
    CONTEXT = ["iban", "рахунок", "bank"]  # Ukrainian context hints

    def __init__(self):
        super().__init__(
            supported_entity="UKR_IBAN",
            patterns=self.PATTERNS,
            name="ukr_iban_recognizer",
            supported_language="uk"
        ) 