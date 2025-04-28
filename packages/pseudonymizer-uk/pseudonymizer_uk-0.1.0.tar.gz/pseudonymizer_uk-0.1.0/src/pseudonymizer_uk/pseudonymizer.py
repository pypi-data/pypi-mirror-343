from typing import Dict, List
import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, EntityRecognizer
from presidio_analyzer.nlp_engine import NerModelConfiguration, SpacyNlpEngine
from presidio_analyzer.predefined_recognizers import (
    EmailRecognizer,
    CreditCardRecognizer,
    PhoneRecognizer,
    UrlRecognizer
)
from presidio_anonymizer import AnonymizerEngine, OperatorConfig

class NerUkSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_spacy_model, entities=['PERSON', 'JOB', 'LOCATION', 'ORGANIZATION', 'DATE_TIME']):
        super().__init__()
        model_to_presidio_entity_mapping = dict(
                PERS= "PERSON",
                LOC= "LOCATION",
                ORG= "ORGANIZATION",
                DATE= "DATE_TIME",
                TIME= "DATE_TIME",
                PERIOD= "DATE_TIME"
        )
        model_to_presidio_entity_mapping = {key: value for key, value in model_to_presidio_entity_mapping.items() if value in entities}
        self.supported_languages = ["uk"]
        self.nlp = {"uk": loaded_spacy_model}

        self.ner_model_configuration = NerModelConfiguration(
            model_to_presidio_entity_mapping=model_to_presidio_entity_mapping,
            labels_to_ignore = ["O"],
            low_score_entity_names=['ORGANIZATION']
        )

class UkPseudonymizer:
    """
    A pseudonymizer specifically designed for Ukrainian text using Presidio analyzer
    with uk_ner_web_trf_13class model and additional recognizers.
    """
        
    def __init__(
        self,
        path_to_model: str = None,
        custom_recognizers: List[EntityRecognizer] = None,
        custom_operators: Dict[str, OperatorConfig] = None,
        entities: List[str] = ['PERSON', 'JOB', 'LOCATION', 'ORGANIZATION', 'DATE_TIME']
    ):
        """
        Initialize the Ukrainian Pseudonymizer with Presidio analyzer and optional custom components.
        
        Args:
            path_to_model: Path to the uk_ner_web_trf_13class model directory
            custom_recognizers: Dictionary of entity type to custom recognition functions
            custom_operators: Dictionary of entity type to custom pseudonymization functions
            entities: List of entity types to recognize
        """
        if path_to_model is None:
            raise ValueError("path_to_model is required")
    
        self.path_to_model = path_to_model
        self.nlp = None
        self.analyzer = None
        
        self.custom_recognizers = custom_recognizers or []
        self.custom_operators = custom_operators or {}
        self.entities = entities
        self._setup_presidio()
        
    def _load_model(self) -> None:
        """Load the NER UK model if it hasn't been loaded yet."""
        if self.nlp is None:
            self.nlp = spacy.load(self.path_to_model)

    def _setup_presidio(self) -> None:
        """Setup Presidio analyzer with Ukrainian NER and additional recognizers."""
        self._load_model()

        # Setup registry and analyzer
        registry = RecognizerRegistry(supported_languages=["uk"])
        registry.load_predefined_recognizers()
        # Add predefined recognizers
        registry.add_recognizer(EmailRecognizer(supported_language="uk"))
        registry.add_recognizer(CreditCardRecognizer(supported_language="uk"))
        registry.add_recognizer(UrlRecognizer(supported_language="uk"))
        registry.add_recognizer(PhoneRecognizer(
            supported_language="uk",
            leniency=3,
            context=["номер телефону"],
            supported_regions=["UA"]
        ))
        for recognizer in self.custom_recognizers:
            registry.add_recognizer(recognizer)

        # Create and setup analyzer with custom NLP engine
        nlp_engine = NerUkSpacyNlpEngine(loaded_spacy_model=self.nlp)
        
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            registry=registry,
            supported_languages=["uk"]
        )
        self.anonymizer = AnonymizerEngine()

    def pseudonymize(self, text: str) -> str:
        """
        Pseudonymize the Ukrainian text using Presidio analyzer and custom operators.
        
        Args:
            text: Input Ukrainian text to pseudonymize
            
        Returns:
            Pseudonymized text with entities replaced according to operators
        """
        results = self.analyzer.analyze(text=text, language="uk")

        if not results:
            return text

        # Sort results by start position in reverse order to handle replacements
        # from end to start (to maintain correct positions)
        results = sorted(results, key=lambda x: x.start, reverse=True)
        # Process entities and replace them
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=self.custom_operators if len(self.custom_operators.items()) > 0 else None
        )

        return anonymized_result

    def add_custom_recognizer(self, recognizer: EntityRecognizer) -> None:
        """Add a custom Presidio recognizer."""
        if self.analyzer:
            self.analyzer.registry.add_recognizer(recognizer)

    def add_custom_operator(self, entity_type: str, config: OperatorConfig) -> None:
        """Add a custom pseudonymization operator."""
        self.custom_operators[entity_type] = config 