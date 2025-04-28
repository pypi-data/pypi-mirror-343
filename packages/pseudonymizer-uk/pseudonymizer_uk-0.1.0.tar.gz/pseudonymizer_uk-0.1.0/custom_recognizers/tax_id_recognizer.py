"""
Ukrainian Tax ID recognizer for Presidio.
"""
from presidio_analyzer.pattern_recognizer import PatternRecognizer
from presidio_analyzer.pattern import Pattern


class UkrTaxIdRecognizer(PatternRecognizer):
    """
    Recognizes Ukrainian Tax ID (ІПН / РНОКПП): ten digits, 
    with optional prefix.
    """
    PATTERNS = [
        # bare 10 digits
        Pattern(name="ten_digits", regex=r"\b\d{10}\b", score=0.5),
        Pattern(name="ten_digits_with_code", regex=r"\b(?:код)[:\s]*\d{10}\b", score=0.6),
        # prefixed forms: ІПН 1234567890 or РНОКПП 1234567890 (colon optional)
        Pattern(
            name="ukr_tax_id_prefixed", 
            regex=r"\b(?:індивідуальний податковий номер|Ідентифікаційний номер|Ідентифікаційний код|ІПН|РНОКПП|Реєстраційний номер облікової картки платника податків)(?::|)[\s]*\d{10}\b",
            score=1.0
        ),
    ]

    CONTEXT = [
        "ІПН",
        "РНОКПП",
        "Ідентифікаційний номер",
        "Ідентифікаційний код",
        "Індивідуальний податковий номер",
        "Реєстраційний номер облікової картки платника податків",
        "Податковий номер",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="UKR_TAX_ID",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="ukr_tax_id_recognizer",
            supported_language="uk"
        ) 