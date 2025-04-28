# Ukrainian Presidio Recognizers

A collection of custom recognizers for Microsoft Presidio designed to detect Ukrainian PII (Personally Identifiable Information) in text. These are static rule-based recognizers that can be used without additional models.

## Installation

```bash
pip install ukr-presidio-recognizers
```

Or from source:

```bash
git clone https://github.com/youruser/ukr-presidio-recognizers.git
cd ukr-presidio-recognizers
pip install -e .
```

## Included Recognizers

The package includes the following recognizers:

1. **UkrIbanRecognizer** - Recognizes Ukrainian IBAN numbers (format: `UAkk XXXXXX XXXXXXXXXXXXXXXXXXX`)
2. **UkrTaxIdRecognizer** - Recognizes Ukrainian Tax ID numbers (РНОКПП/ІПН, 10 digits)
3. **UkrLicensePlateRecognizer** - Recognizes Ukrainian car license plates
4. **UkrMilitaryUnitRecognizer** - Recognizes Ukrainian military unit identifiers:
   - Armed Forces (в/ч A1234) - Cyrillic letter + 4 digits
   - National Guard (в/ч 2837) - 4 digits
5. **UkrEdrpouRecognizer** - Recognizes Ukrainian ЄДРПОУ numbers

## Usage

Since these recognizers are pattern-based and do not rely on NLP processing, there are two main ways to use them:

### Option 1: Using ad_hoc_recognizers

This option avoids the `KeyError: 'uk'` error that occurs because Presidio doesn't have built-in Ukrainian language support:

```python
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from ukr_presidio_recognizers import (
    UkrIbanRecognizer,
    UkrTaxIdRecognizer,
    UkrLicensePlateRecognizer,
    UkrMilitaryUnitRecognizer,
    UkrEdrpouRecognizer
)

# Create a registry
registry = RecognizerRegistry()

# Use English NLP engine to avoid errors
nlp_configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
}
nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()

# Create an analyzer with the registry
analyzer = AnalyzerEngine(registry=registry, nlp_engine=nlp_engine)

# Analyze text using ad_hoc_recognizers
text = "IBAN UA933220010000026207301340795, РНОКПП 3706310677, номер машини ВС3668ТО, військова частина A1126, НГУ 2837"
results = analyzer.analyze(
    text=text, 
    language="en",  # Use English as base language
    ad_hoc_recognizers=[  # Pass our recognizers directly
        UkrIbanRecognizer(),
        UkrTaxIdRecognizer(),
        UkrLicensePlateRecognizer(),
        UkrMilitaryUnitRecognizer(),
        UkrEdrpouRecognizer()
    ]
)

# Print results
for result in results:
    print(f"{result.entity_type}: {text[result.start:result.end]} (confidence: {result.score})")
```

### Option 2: Using recognizers directly

You can also use each recognizer individually, which is the simplest approach:

```python
from ukr_presidio_recognizers import (
    UkrIbanRecognizer,
    UkrTaxIdRecognizer,
    UkrLicensePlateRecognizer,
    UkrMilitaryUnitRecognizer,
    UkrEdrpouRecognizer
)

text = "IBAN UA933220010000026207301340795, РНОКПП 3706310677, номер машини ВС3668ТО, військова частина A1126, НГУ 2837"

# Create recognizer instances
recognizers = [
    UkrIbanRecognizer(),
    UkrTaxIdRecognizer(),
    UkrLicensePlateRecognizer(),
    UkrMilitaryUnitRecognizer(),
    UkrEdrpouRecognizer()
]

# Use each recognizer directly
for recognizer in recognizers:
    results = recognizer.analyze(text=text, entities=[recognizer.supported_entity])
    for result in results:
        print(f"{result.entity_type}: {text[result.start:result.end]} (confidence: {result.score})")
```

## License

MIT 