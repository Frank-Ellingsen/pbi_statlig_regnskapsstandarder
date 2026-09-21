# Power BI stjernemodell

## Import
Importer alle CSV-filene som UTF-8 med semikolon som skilletegn. Sett DatoNokkel til heltall i alle tabeller. Sett belop, studiepoeng og arsverk til desimaltall.

## Modell
Opprett relasjonene i `Relationships.csv`. Alle relasjoner skal være aktive, mange-til-en fra faktatabell til dimensjon og ha enkel filtreringsretning fra dimensjon til fakta. Ikke bruk toveis filtrering.

## Organisasjonshierarki
I `DimOrganization` oppretter du hierarkiet `UiA organisasjon`: OrgNavn > Instituttnavn > Koststednavn. Finansfakta ligger på koststed. Arsverk og studiepoeng bruker egne institutt-totalmedlemmer med koststedtype `Institutt total`.

## Andre hierarkier
- Konto: SRS_regnskapslinje > Kontotype > Kontonavn > Konto
- Prosjekt: Finansieringstype > Finansieringskilde > Prosjektkategori > Prosjektnavn
- Studie: Studienivaa > Studieprogramnavn
- Tid: Aar > Kvartal > Maaned > Dato

## Viktig modelleringsvalg
Studiepoeng og arsverk ligger i egne faktatabeller. De skal ikke summeres ukritisk over dato. For manedsstatus kan du bruke siste periode i filterkonteksten, mens produksjon som avlagte studiepoeng kan summeres YTD.
