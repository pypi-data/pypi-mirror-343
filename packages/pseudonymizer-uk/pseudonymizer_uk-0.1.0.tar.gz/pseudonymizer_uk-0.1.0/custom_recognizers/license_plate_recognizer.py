"""
Ukrainian License Plate recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrLicensePlateRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian car license plates (two letters, four digits, two letters).
    The letters can be either Latin or Cyrillic.
    """
    PATTERNS = [
        Pattern(
            name="plate_compact",
            regex=r"\b[ABEIKMHOPCTXDIАВЕІКМНОРСТХІ]{2}\d{4}[ABEIKMHOPCTXYZIАВЕІКМНОРСТХУІ]{2}\b",
            score=1.0,
        ),
        Pattern(
            name="plate_spaced", 
            regex=r"\b[ABEIKMHOPCTXDIАВЕІКМНОРСТХІ]{2}\s?\d{4}\s?[ABEIKMHOPCTXYZIАВЕІКМНОРСТХУІ]{2}\b",
            score=1.0,
        ),
    ]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_LICENSE_PLATE",
            patterns=self.PATTERNS,
            name="ukr_license_plate_recognizer",
            supported_language="uk"
        ) 