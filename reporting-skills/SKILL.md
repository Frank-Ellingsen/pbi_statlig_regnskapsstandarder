---
name: uia-kontroll-og-rapportering
description: >-
  Veileder og faglig regelverk for controlling, økonomistyring og rapportering ved Universitetet i Agder (UiA).
  Bruk denne ferdigheten når du analyserer statlig regnskap (SRS 1, 9, 10, 17), vurderer KD finansieringsmodellen 2025,
  beregner studiepoengsatser (SPE60 Kat 1/2/3), kontrollerer 5 %-regelen for ubrukte bevilgningsmidler (F-05-20),
  gjennomfører prosjektcontrolling for BOA etter TDI-modellen, tertialrapportering (T1/T2/LE) og Note 15.
---

# Controller- og Rapporteringsferdigheter ved Universitetet i Agder (UiA)

Denne ferdigheten standardiserer og profesjonaliserer controllerfunksjonen ved Universitetet i Agder (UiA) og tilsvarende statlige utdanningsinstitusjoner. Som seniorcontroller fungerer du som strategisk beslutningsstøtte og økonomisk problemløser som transformerer komplekse regnskapsdata til handlingsrettet styringsinformasjon.

---

## 1. Rettslig og Regulatorisk Rammeverk

### 1.1 KD Finansieringsmodell 2025 & Studiepoengsatser (SPE60)
Fra 2025 innfører Kunnskapsdepartementet (KD) en ny finansieringsmodell:
* **Basisbevilgning**: Tidligere lukkede resultatindikatorer (publisering, EU-midler, NFR-midler, BOA-resultater) er innlemmet i basisbevilgningen basert på et 3-årig gjennomsnitt (2020–2022).
* **Åpen ramme (Resultatbasert uttelling)**: Antall studiepoengkategorier er redusert fra 6 til 3.
  * **Kategori 1 (54 550 NOK / 60 SPE)**: Humaniora, samfunns- og økonomifag.
  * **Kategori 2 (81 800 NOK / 60 SPE)**: Realfag, helse-, sosial- og lærerutdanninger (inkl. profesjonsstudiet i psykologi).
  * **Kategori 3 (190 900 NOK / 60 SPE)**: Medisin, odontologi og veterinærmedisin.

> [!CRITICAL]
> **Kritisk kontrollpunkt (Volumvarsel / Marginalitetsprinsipp):**
> De nye satsene skal **kun** benyttes ved marginale endringer i produksjon eller ved tildeling av nye studieplasser. Eksisterende studieplasser er beskyttet av nettobudsjetteringsprinsippet og skal **ikke** devalueres ved å anvende nye satser på historisk volum. Bruk aldri nye satser til å regne ned grunnbevilgningen for eksisterende aktivitet.

### 1.2 Statlige Regnskapsstandarder (SRS)
All regnskapsførsel skjer etter opptjeningsprinsippet (SRS):
| Standard | Beskrivelse & Anvendelse ved UiA |
| :--- | :--- |
| **SRS 1** | Presentasjon av virksomhetsregnskapet. Sikrer konsistent oppstilling av opptjening og kostnader. |
| **SRS 9** | Inntekt fra transaksjonsbaserte hendelser. Benyttes for **Oppdragsaktivitet** (fullføringsgrad/leverte tjenester). |
| **SRS 10** | Inntekt fra bevilgninger og tilskudd. Benyttes for **Bidragsaktivitet** (motsatt sammenstilling: inntekt = påløpt kostnad). |
| **SRS 17** | Anleggsmidler. Kontroll av investeringsplaner, aktiveringskriterier og korrekte lineære avskrivninger. |

### 1.3 5 %-regelen for Ubrukte Midler (Rundskriv F-05-20) & Anskaffelser
* **5 %-regelen**: Akkumulert mindreforbruk / ubrukte bevilgningsmidler utover **5,0 % av årlig tildeling** kan kreves tilbakeført til statskassen eller medføre kutt i fremtidige rammer.
  $$\text{Akkumulert Mindreforbruk \%} = \frac{\text{Ubrukte midler per 31.12}}{\text{Årsbevilgning}} \times 100$$
  * *Terskel*: Dersom mindreforbruket overstiger 5,0 %, må det utarbeides en formell tiltaks- og investeringsplan for styret og departementet (begrunnes i Note 15).
* **Offentlige anskaffelser (FOA)**:
  * Under 500 000 kr: Dokumentert reelt behov og dokumentert konkurranseutsetting.
  * Over 500 000 kr: Krav om formell anskaffelsesprotokoll, utvidet dokumentasjon og bruk av felles rammeavtaler.

---

## 2. Operasjonelle Kontrollfunksjoner & Internkontroll

### 2.1 BOA-prosjektcontrolling via TDI-modellen
BOA-prosjekter (Bidrag og Oppdrag) følges opp etter **TDI-modellen**:
$$\text{Totalkostnad} = \text{Tid (T)} + \text{Direkte kostnader (D)} + \text{Indirekte kostnader / Overhead (I)}$$

| Egenskap | Bidragsaktivitet (B) | Oppdragsaktivitet (O) |
| :--- | :--- | :--- |
| **Hovedregel** | Samfunnsoppdrag / forskningsstøtte (NFR, EU Horizon). | Tjenestesalg med direkte motytelse til oppdragsgiver. |
| **Regnskapsstandard** | **SRS 10**: Inntekt = påløpte kostnader. Ingen fortjeneste. | **SRS 9**: Inntekt inntektsføres etter fremdrift / fullføringsgrad. |
| **Frikjøp** | Kontroller at timer belastet prosjektet samsvarer med faktisk frigitt undervisningstid. | Full kostnadsdekning + kalkulert fortjenestemargin. |
| **Overhead** | Dekkes ofte delvis av finansiør; krever kontroll av institusjonens egenfinansiering. | Skal fullt ut dekke alle institusjonens indirekte kostnader. |

### 2.2 RAG Risikostyring (FactAction)
Risiko og tiltak følges opp med RAG-status i `FactAction`:
* 🟢 **Grønn**: Planmessig drift. Avvik $\le 2\%$.
* 🟡 **Gul**: Moderat avvik (2–5 %). Krever observasjon og interne budsjettjusteringer.
* 🔴 **Rød**: Vesentlig avvik ($> 5\%$) eller forsinket tiltak. Krever umiddelbar skriftlig rapport til dekan/direktør og formell budsjettomdisponering.

---

## 3. Budsjettprosess & Tertialvis Rapporteringskadens

### 3.1 Årshjulet for Controlling
1. **Budsjett**: Fastsettelse av rammer og periodisert månedsbudsjett.
2. **Regnskap (Actuals)**: Månedlig periodisering og balansekontroll.
3. **Avviksanalyse**: Identifisering av kostnadsdrivere (lønn, drift, investering).
4. **Prognose (LE - Latest Estimate)**: Realistisk forventning til årsresultat basert på faktisk regnskap YTD + oppdaterte forutsetninger for reståret.
5. **Tiltak (`FactAction`)**: Korrigerende handlinger med kvantifisert effekt for å lukke gapet til budsjett.

### 3.2 Rapporteringshierarki
* **Instituttleder**: Operasjonell drift, student/årsverk-forhold, lokalt lønnsforbruk.
* **Dekan & Fakultetsledelse**: Porteføljestyring, samlet fakultetsmargin, tiltaksgjennomføring.
* **Universitetsdirektør**: Likviditet, samlet bemanningsutvikling, tverrgående risikobilde.
* **Universitetsstyret**: Strategisk måloppnåelse, 5 %-regel etterlevelse, tertialrapporter og årsregnskap.

### 3.3 Note 15 & Årsavslutning
Ved årsslutt kvalitetssikrer controlleren **Note 15 i virksomhetsregnskapet**:
* Avstemmer årets regnskapsmessige resultat mot bevilgningsregnskapet.
* Dokumenterer disponering av ubrukte midler opp mot 5 %-regelen.
* Begrunner bindinger for flerårige investeringer og prosjektforpliktelser.

---

## 4. Edward Tufte Data-Ink Standard for Rapportering
* **Fjern unødvendig støy**: Ingen vertikale tabellinjer, ingen tunge 3D-kanter eller skygger.
* **Fokusert fargebruk**: Nøytral palett (skifer/mørkeblå), med kraftig rød/gul fargeheving kun for aktive avvik og overskridelser.
* **Talljustering**: Tekst venstrejusteres, tall høyrejusteres, desimaler justeres vertikalt.

---

## 5. Tilhørende Ressurser & Referanser
* 📄 [Full Veileder for UiA (Markdown)](./references/veileder_kontroll_og_rapportering_uia.md)
* 📄 [KD Finansieringsmodell 2025 Retningslinjer](./references/kd_finansieringsmodell_2025.md)
* 📄 [Statlige Regnskapsstandarder (SRS 1, 9, 10, 17)](./references/statlige_regnskapsstandarder_srs.md)
* 📄 [BOA & TDI Modellen](./references/boa_tdi_modell.md)
* 📄 [5 %-regelen & Note 15 Veiledning](./references/femprosent_regelen_og_note15.md)
* 📄 [Controller Kompetansekart](./references/controller_kompetansekart.md)
* 🐍 [Verifiseringsskript for Rapporteringsregler](./scripts/verify_reporting_rules.py)
