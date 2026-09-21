# Forecast-modell for Power BI

## Grain
`FactForecast` har én rad per måned, organisasjonsnøkkel, konto, prosjekt og forecastversjon.

## Versjoner
- FC1_2026: faktisk januar-april + estimert mai-desember
- FC2_2026: faktisk januar-august + estimert september-desember
- LE_2026: faktisk januar-oktober + estimert november-desember

## Relasjoner
Legg inn de fem nye relasjonene fra `Relationships_Forecast.csv`. Alle skal være 1:* og ha enkel filtreringsretning fra dimensjon til fakta.

## Versjonsvalg
Bruk `DimForecastVersion[Versjonsnavn]` som slicer. Sett enkeltvalg på. DAX-målene bruker LE_2026 som standard hvis ingen versjon er valgt.

## Fortegn
ForecastBelop følger samme fortegn som FactGL: kostnader er positive, inntekter negative. Inntektsmålene snur derfor fortegnet.

## Tiltak
`Tiltakseffekt` er satt til null i mockdata. Negative tiltakseffekter reduserer kostnadsforecast, mens positive effekter øker kostnaden. For inntekter må effekten følge datamodellens fortegn.

## Viktig
Dataene er syntetiske treningsdata. Modellen representerer ikke UiAs operative forecast eller kontoplan.
