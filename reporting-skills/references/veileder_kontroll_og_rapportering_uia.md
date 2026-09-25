# Veileder for kontroll og rapportering ved Universitetet i Agder (UiA)

## 1. Innledning og formål
Denne veilederen er utarbeidet for å profesjonalisere og standardisere controllerfunksjonen ved Universitetet i Agder (UiA). Som controller ved UiA fungerer du som en strategisk beslutningsstøtte og en "økonomisk problemløser" som opererer på tvers av organisatoriske grenser.

Formålet er å sikre etterlevelse av statlig regelverk og bidra til robuste prognoser som gir ledelsen reelt handlingsrom. Controllerens rolle er å transformere komplekse regnskapsdata til styringsinformasjon, slik at universitetet kan oppfylle sitt samfunnsoppdrag innen utdanning og forskning på en økonomisk bærekraftig måte.

---

## 2. Rettslig og regulatorisk rammeverk

### 2.1 Universitets- og høyskoleloven (UHL) og finansieringsmodellen
UiA styres etter prinsippet om nettobudsjettering. Styret har det overordnede ansvaret for at ressursbruken er effektiv og i tråd med gitte rammer. Fra 2025 innfører Kunnskapsdepartementet (KD) en ny finansieringsmodell som forenkler dagens system betydelig.

#### Viktige endringer i finansieringsmodellen (fra 2025):
* **Basisbevilgning (Styrket)**: Tidligere "lukkede rammer" (publisering, EU-midler, NFR-midler og BOA-resultater) avvikles som egne resultatindikatorer. Disse er nå innlemmet i basisbevilgningen, basert på et treårig gjennomsnitt (2020–2022) for å sikre stabilitet.
* **Åpen ramme (Resultatbasert)**: Antall kategorier for studiepoengutveksling reduseres fra seks til tre. Følgende satser per 60 studiepoeng (SPE) gjelder for endring i produksjon:
  * **Kategori 1 (54 550 NOK)**: Humaniora, samfunns- og økonomifag.
  * **Kategori 2 (81 800 NOK)**: Realfag, helse-, sosial- og lærerutdanninger (inkl. profesjonsstudiet i psykologi).
  * **Kategori 3 (190 900 NOK)**: Medisin, odontologi og veterinærmedisin.

> [!WARNING]
> **Kritisk kontrollpunkt (Volumvarsel / Marginalitetsprinsipp):**  
> Som seniorcontroller må du påse at de nye satsene **kun benyttes ved marginale endringer i produksjon eller tildeling av nye studieplasser**. Eksisterende studieplasser er beskyttet av nettobudsjetteringsprinsippet og skal **ikke** devalueres ved å anvende de nye satsene på gammelt volum. En feilaktig bruk av disse satsene på eksisterende volum vil undervurdere de reelle kostnadene og svekke enhetenes økonomiske bærekraft.

### 2.2 Statens økonomiregelverk og Virksomhetsinstruks
All økonomistyring skal skje i henhold til **Reglement for økonomistyring i staten §§ 4 og 14**. Dette innebærer at controlleren har et særskilt ansvar for å operere innenfor rammene i KDs årlige tildelingsbrev og universitetets interne virksomhetsinstruks. Krav til nøyaktighet, integritet og sporbarhet er ufravikelige.

### 2.3 Regnskapsstandarder (SRS) og Periodisering
UiA følger de statlige regnskapsstandardene (SRS) med periodisering som hovedprinsipp.

| Standard | Tittel | Beskrivelse og operasjonell relevans |
| :--- | :--- | :--- |
| **SRS 1** | Presentasjon av virksomhetsregnskapet | Sikrer konsistent oppstilling og sammenlignbarhet over tid. |
| **SRS 9** | Inntekt fra transaksjonsbaserte hendelser | Brukes for **Oppdragsaktivitet** (fullføringsgrad/leverte tjenester). |
| **SRS 10** | Inntekt fra bevilgninger og tilskudd | Brukes for **Bidragsaktivitet** (motsatt sammenstilling: inntekt = påløpt kostnad). |
| **SRS 17** | Anleggsmidler | Kontroll av investeringsplaner, aktiveringskriterier og korrekte avskrivninger. |

### 2.4 Anskaffelser og Avsetningsreglement
* **5 %-regelen (Rundskriv F-05-20)**: Ubrukte midler utover **5 % av bevilgningen** kan kreves tilbakeført til statskassen eller medføre reduksjon i fremtidige rammer. Controlleren må overvåke akkumulerte mindreforbruk nøye mot årets slutt.
* **Offentlige anskaffelser (FOA)**:
  * For kjøp under 500 000 kr: Krav om dokumentert reelt behov og dokumentert konkurranseutsetting.
  * For kjøp over 500 000 kr: Krav om protokoll, utvidet dokumentasjon og bruk av felles rammeavtaler der de finnes.

---

## 3. Operasjonelle kontrollfunksjoner og Internkontroll

### 3.1 Arbeidsdeling og systemrutiner (BOTT / Unit4 ERP)
I Unit4 ERP (BtB-modulen) skal controlleren fungere som en kvalitetssikrer av prosessene. Din rolle er ikke primært å utføre transaksjoner, men å overvåke at arbeidsdelingen mellom attestant og anviser fungerer, og at rutiner for fakturering og timelønn etterleves. Ved systematiske feil skal du initiere prosessforbedring fremfor enkelttilrettelegging.

### 3.2 Prosjektcontrolling i BOA (Bidrag og Oppdrag)
BOA-prosjekter følges opp via **TDI-modellen** (Tid, Direkte kostnader, Indirekte kostnader).

| Egenskap | Bidragsaktivitet (B) | Oppdragsaktivitet (O) |
| :--- | :--- | :--- |
| **Hovedregel** | Samfunnsoppdrag / støtte (EU / NFR). | Tjenestesalg med motytelse. |
| **Regnskap** | SRS 10 (Inntekt = Påløpt kostnad). | SRS 9 (Inntekt føres etter fremdrift). |
| **Frikjøp** | Viktig: Verifiser at timer belastet prosjekt samsvarer med faktisk frigitt tid fra undervisning. | Full kostnadsdekning + fortjeneste. |
| **Overhead** | Dekkes ofte delvis; krever kontroll av institusjonens egenfinansiering. | Skal dekke alle indirekte kostnader. |

### 3.3 Balanse- og periodiseringskontroll
Månedlig kontroll av balansen er nødvendig for å fange opp ikke-inntektsførte bevilgninger. Spesielt viktig er avstemming av prosjektbeholdninger og kontroll av at avskrivningsplaner (SRS 17) er i tråd med eiendelenes faktiske levetid.

### 3.4 Risikostyring og avviksoppfølging
Vi benytter RAG-status (Red-Amber-Green) i `FactAction` for å visualisere økonomisk risiko:
* 🟢 **Grønn**: Planmessig drift.
* 🟡 **Gul**: Avvik som krever observasjon og interne justeringer.
* 🔴 **Rød**: Vesentlig risiko eller avvik. Krever umiddelbar skriftlig rapport til dekan/direktør og vurdering av formell budsjettjustering.

---

## 4. Budsjettprosess og Prognosearbeid

### 4.1 Koordinering av budsjett
Controlleren koordinerer prosessen fra rammeavklaring til ferdigstilt fakultetsbudsjett. Vi følger logikken:  
$$\text{Budsjett} \longrightarrow \text{Regnskap} \longrightarrow \text{Avviksanalyser} \longrightarrow \text{Prognose (LE)} \longrightarrow \text{Tiltak}$$

### 4.2 Kvalitetssikring av forutsetninger
Still alltid disse spørsmålene før budsjett og LE låses:
1. Er lønnsbudsjettet basert på faktisk bemanning og kjente nyansettelser (frikjøp inkludert)?
2. Er forutsetningene konsistente mellom instituttene og fakultetets totalramme?
3. Mangler det bindinger for fremtidige forpliktelser i prosjektporteføljen?
4. Er datagrunnlaget tilstrekkelig for at ledelsen kan ta beslutninger om f.eks. ansettelsesstopp eller investeringer?

---

## 5. Rapporteringskadens og Hierarki

### 5.1 Tertialvis oppfølging (T1, T2, LE)
Rapporteringen skjer per tertial med fokus på **Latest Estimate (LE)**. LE skal representere den mest realistiske forventningen til årsresultatet, basert på Actuals (regnskap per dato) og oppdaterte forutsetninger for resten av året.

### 5.2 Målgruppetilpasset rapportering
Data fra Unit4 transformeres i Power BI og Excel til visuelle dashboards. Rapporteringen følger linjen:  
$$\text{Instituttleder} \longrightarrow \text{Dekan} \longrightarrow \text{Universitetsdirektør} \longrightarrow \text{Styret}$$  
Fokuser på trender og forklaring av avvik fremfor rådata.

### 5.3 Årsrapport og Virksomhetsregnskap
Ved årsslutt er controlleren ansvarlig for bidrag til styrets beretning og **Note 15**. Note 15 er avgjørende da den viser avstemmingen av årets resultat og forklarer bruken av "ubrukte midler". Her må det dokumenteres hvordan universitetet forholder seg til 5 %-regelen og begrunne eventuelle avsetninger til fremtidige investeringer.

---

## 6. Prosessforbedring og Dokumentasjon
Som seniorcontroller er du en pådriver for effektive arbeidsrutiner. Ryddig dokumentasjon er fundamentet for vår integritet og sporbarhet (f.eks. ved revisjon fra Riksrevisjonen).

### Veien fra teknikk til beslutningsstøtte:
* **Excel / Power Query**: Automatiser databehandling for å eliminere manuelt dobbeltarbeid.
* **Analyse**: Gå bak tallene. Hvis reisekostnadene er lave, er det en reell besparelse eller bare forsinket fakturering?
* **Beslutningsstøtte**: Presenter alltid et handlingsrom. Ikke bare konstater avviket, men foreslå om midler bør omdisponeres eller om aktiviteten må bremses.

> [!TIP]
> **Dokumentasjonskjeden:**  
> $\text{Datagrunnlag} \longrightarrow \text{Forutsetninger} \longrightarrow \text{Beregning} \longrightarrow \text{Analyse} \longrightarrow \text{Anbefaling}$
