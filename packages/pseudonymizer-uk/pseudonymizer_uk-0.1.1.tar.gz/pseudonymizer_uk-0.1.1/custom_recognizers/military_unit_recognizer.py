"""
Ukrainian Military Unit recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrMilitaryUnitRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian military unit identifiers.
    
    Ukrainian military units typically have two formats:
    1. Armed Forces (ЗСУ): "в/ч A1234" - a Cyrillic letter (usually A) followed by 4 digits
    2. National Guard (НГУ): "в/ч 2837" - just 4 digits without a letter prefix
    """
    PATTERNS = [
        # Format: в/ч A1234 (Armed Forces)
        Pattern(
            name="military_unit_basic_armed_forces",
            regex=r"\bв/?ч\s*[A-ZА-ЯІЇҐЄ]\d{1,4}\b",
            score=0.7,
        ),
        # Format with additional details: військова частина A1234
        Pattern(
            name="military_unit_full_armed_forces", 
            regex=r"\bвійськов(?:а|ої|у|ою)\s*части(?:на|ни|ні|ну|ною)\s*[A-ZА-ЯІЇҐЄ]\d{1,4}\b",
            score=0.8,
        ),
        # Format with just the code: A1234 (Armed Forces)
        Pattern(
            name="military_unit_code_armed_forces",
            regex=r"\b[AА]\d{4}\b",
            score=0.5,
        ),
        # Format: в/ч 2837 (National Guard)
        Pattern(
            name="military_unit_basic_national_guard",
            regex=r"\bв/?ч\s*\d{4}\b",
            score=0.7,
        ),
        # Format with additional details: військова частина 2837 (National Guard)
        Pattern(
            name="military_unit_full_national_guard", 
            regex=r"\bвійськов(?:а|ої|у|ою)\s*части(?:на|ни|ні|ну|ною)\s*\d{4}\b",
            score=0.8,
        ),
        # Format in National Guard context: НГУ 2837 or Національна гвардія 2837
        Pattern(
            name="military_unit_ngu_context",
            regex=r"\b(?:НГУ|[Нн]аціональн(?:а|ої|ій|у|ою)\s*[Гг]вард(?:ія|ії|ії|ію|ією))\s*\d{4}\b",
            score=0.9,
        ),
    ]
    
    CONTEXT = ["військова", "частина", "в/ч", "національна", "гвардія", "НГУ", "ЗСУ"]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_MILITARY_UNIT",
            patterns=self.PATTERNS,
            name="ukr_military_unit_recognizer",
            supported_language="uk",
            context=self.CONTEXT
        )