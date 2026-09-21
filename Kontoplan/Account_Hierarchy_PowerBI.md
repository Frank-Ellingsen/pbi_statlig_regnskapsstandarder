# Kontoplanhierarki i Power BI

Anbefalt dimensjon i modellen: `DimAccountHierarchy` som én denormalisert kontodimensjon. Opprett hierarkiet:
1. `Nivaa1_Navn` (kontoklasse)
2. `Nivaa2_Navn` (kontogruppe)
3. `Nivaa3_Navn` (obligatorisk standardkonto, 3 siffer)
4. `Nivaa4_Navn` / `Konto` (intern underkonto, 4+ siffer)

Behold `DimAccountClass` og `DimAccountGroup` som oppslag/dokumentasjon, men unngå snowflake-relasjoner i semantic model med mindre det er et spesifikt behov. Fact-tabellene relateres 1:* fra `DimAccountHierarchy[Konto]` til faktaenes `Konto`.

Merk: Standard kontoplan R-102 har kontoklasse 1-8. Kontoklasse 9 er inkludert kun som intern/valgfri klasse og skal ikke behandles som en offisiell R-102-kontoklasse.
