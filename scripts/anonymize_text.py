import os
import re

def anonymize_file(filepath, extra_replacements=None):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    replacements = [
        ("Universitetet i Agder (UiA)", "Statlig utdanningsinstitusjon"),
        ("Universitetet i Agder", "Statlig utdanningsinstitusjon"),
        ("UiA Controller & Forecast Portal", "Statlig Utdanningsinstitusjon - Controller & Forecast Portal"),
        ("UiA Controller - Helhetlig Virksomhetsstyring & Forecast Datamodell", "Statlig Utdanningsinstitusjon - Helhetlig Virksomhetsstyring & Forecast Datamodell"),
        ("UiA Controller", "Controller"),
        ("UiA-modellen", "modellen"),
        ("UiAs", "institusjonens"),
        ("UiA-struktur", "organisasjonsstruktur"),
        ("UiA organisasjon", "Organisasjonshierarki"),
        ("Handelshøyskolen ved UiA", "Handelshøyskolen"),
        ("Handelshøyskolen UiA", "Handelshøyskolen"),
        ("for hele UiA", "for hele institusjonen"),
        ("Hele UiA", "Hele institusjonen"),
        ("Totalt UiA", "Totalt institusjonen"),
        ("Gj.snitt UiA", "Gj.snitt institusjonen"),
        ("Årsbudsjett UiA", "Årsbudsjett (Institusjonen)"),
        ("Totalbudsjett UiA", "Totalbudsjett"),
        ("Campus Kristiansand", "Campus Hoved"),
        ("Campus Grimstad", "Campus Nord"),
        ("Kristiansand", "Campus Hoved"),
        ("Sustainable Business Models Agder", "Sustainable Business Models Regional Case"),
        ("Agder", "Region"),
        ("uia-logo-badge", "inst-logo-badge"),
        (">UiA<", ">SUI<"),
        (" UiA ", " institusjonen "),
        (" UiA.", " institusjonen."),
        (" UiA,", " institusjonen,"),
        ("(UiA)", "(Institusjonen)"),
    ]

    if extra_replacements:
        replacements.extend(extra_replacements)

    for old, new in replacements:
        text = text.replace(old, new)

    # Clean any stray UiA
    text = re.sub(r'\bUiA\b', 'Institusjonen', text)
    text = re.sub(r'\buia\b', 'institusjonen', text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    remaining = re.findall(r'(?i)\b(uia|universitetet i agder|agder|kristiansand|grimstad)\b', text)
    print(f"Anonymized {filepath} -> Remaining occurrences: {len(remaining)} {set(remaining)}")

if __name__ == "__main__":
    anonymize_file("index.html")
    anonymize_file("README.md")
    anonymize_file("docs/DATA_MODEL_ARCHITECTURE.md")
    anonymize_file("docs/UIA_Controller_Reporting_Suite.md")
    anonymize_file("docs/PowerBI_Model_Setup.md")
    anonymize_file("docs/skills.md")
    anonymize_file("dax/Complete_Measures.dax")
    anonymize_file("dax/All_Measures_Combined.dax")
