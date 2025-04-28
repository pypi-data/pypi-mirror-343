from pseudonymizer import UkPseudonymizer
from presidio_analyzer import Pattern, PatternRecognizer
from presidio_anonymizer import OperatorConfig
import hashlib
from custom_recognizers.tax_id_recognizer import UkrTaxIdRecognizer

def main():
    # Create pseudonymizer instance
    pseudonymizer = UkPseudonymizer()
    
    text = """
    за касаційною скаргою Мельника Олексія Сергійовича (ідентифікаційний номер 1234567890) на рішення Білгород-Дністровського міськрайонного суду Одеської області від 16 серпня 2023 року та постанову Одеського апеляційного суду від 8 грудня 2023 року
    """

    result = pseudonymizer.pseudonymize(text)

    print("\nOriginal text:")
    print(text)
    print("\nPseudonymized text (default masking):")
    print(result)

    # Example 2: Custom operators
    print("\nExample 2: Custom operators")
    
    # Add custom operators
    pseudonymizer.add_custom_operator(entity_type="PERSON", config=OperatorConfig("replace", {"new_value": "ОСОБА"}))
    
    result2 = pseudonymizer.pseudonymize(text)
    print("\nOriginal text:")
    print(text)
    print("\nPseudonymized text (with custom operators):")
    print(result2)

    # Example 3: Adding custom recognizer
    print("\nExample 3: Custom recognizer for Ukrainian tax number")
        
    pseudonymizer.add_custom_recognizer(UkrTaxIdRecognizer())
    pseudonymizer.add_custom_operator("UKR_TAX_ID", OperatorConfig("replace", {"new_value": "ІПН"}))
    
    result3 = pseudonymizer.pseudonymize(text)
    print("\nOriginal text:")
    print(text)
    print("\nPseudonymized text (with custom tax number recognizer):")
    print(result3)


if __name__ == "__main__":
    main()