# Periodic Adverse Drug Experience Report (PADER-style)

**Product:** Bisoprolol  

**Reporting period:** 2024-12-27 to 2025-12-26  

**Report generated:** 2026-08-15 (Version 0 prototype)  

**Data note:** 1068 rows deduplicated to 1024 unique cases via safetyreportid. occurcountry (chosen over primarysource_reportercountry; usually identical, occasionally differs).


## Narrative Summary and Analysis

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52d9ZEXZfYR7sYe19YL'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'Narrative Summary and Analysis':]
{
  "reporting_period": {
    "start": "2024-12-27",
    "end": "2025-12-26"
  },
  "case_volume": {
    "total_cases": 1024,
    "serious_cases": 1023,
    "non_serious_cases": 1,
    "serious_pct": 99.9
  },
  "top_reactions_overall": {
    "Acute kidney injury": 81,
    "Drug ineffective": 60,
    "Hypotension": 48,
    "Drug interaction": 45,
    "Dizziness": 40
  },
  "top_countries": {
    "Eu": 332,
    "United Kingdom": 278,
    "France": 186,
    "Canada": 55,
    "Italy": 52,
    "Germany": 35,
    "Spain": 26,
    "Poland": 20,
    "Portugal": 9,
    "Unknown": 7
  },
  "outcomes": {
    "recovered/resolved": 145,
    "recovering/resolving": 82,
    "recovered/resolved,recovered/resolved": 75,
    "not recovered/not resolved/ongoing": 66,
    "unknown": 61,
    "recovered/resolved,recovered/resolved,recovered/resolved": 50,
    "unknown,unknown": 34,
    "recovering/resolving,recovering/resolving": 29,
    "recovered/resolved,recovered/resolved,recovered/resolved,recovered/resolved": 26,
    "unknown,unknown,unknown": 22
  }
}


## Summary Analysis of Cases

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52dCxdD2PSvyvAtRmyr'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'Summary Analysis of Cases':]
{
  "case_volume": {
    "total_cases": 1024,
    "serious_cases": 1023,
    "non_serious_cases": 1,
    "serious_pct": 99.9
  },
  "seriousness_breakdown": {
    "Death": 67,
    "Life-threatening": 105,
    "Hospitalization": 482,
    "Disabling": 44,
    "Congenital anomaly": 7,
    "Other medically important": 904
  },
  "demographics": {
    "sex": {
      "female": 503,
      "male": 493,
      "Unknown": 28
    },
    "age_group": {
      "65+ (Elderly)": 675,
      "18-64 (Adult)": 249,
      "Unknown": 84,
      "2-11 (Child)": 9,
      "12-17 (Adolescent)": 6,
      "0-1 (Neonate/Infant)": 1
    },
    "top_countries": {
      "Eu": 332,
      "United Kingdom": 278,
      "France": 186,
      "Canada": 55,
      "Italy": 52,
      "Germany": 35,
      "Spain": 26,
      "Poland": 20,
      "Portugal": 9,
      "Unknown": 7
    }
  },
  "outcomes": {
    "recovered/resolved": 145,
    "recovering/resolving": 82,
    "recovered/resolved,recovered/resolved": 75,
    "not recovered/not resolved/ongoing": 66,
    "unknown": 61,
    "recovered/resolved,recovered/resolved,recovered/resolved": 50,
    "unknown,unknown": 34,
    "recovering/resolving,recovering/resolving": 29,
    "recovered/resolved,recovered/resolved,recovered/resolved,recovered/resolved": 26,
    "unknown,unknown,unknown": 22
  }
}


## Reaction/Adverse Event Analysis

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52dGB6UzBEVR7P2CpcG'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'Reaction/Adverse Event Analysis':]
{
  "top_reactions_overall": {
    "Acute kidney injury": 81,
    "Drug ineffective": 60,
    "Hypotension": 48,
    "Drug interaction": 45,
    "Dizziness": 40,
    "Bradycardia": 39,
    "Dyspnoea": 39,
    "Fatigue": 35,
    "Off label use": 34,
    "Diarrhoea": 33,
    "Fall": 32,
    "Condition aggravated": 30,
    "Asthenia": 28,
    "Hypokalaemia": 27,
    "Medication error": 27
  },
  "top_reactions_serious_cases": {
    "Acute kidney injury": 81,
    "Drug ineffective": 59,
    "Hypotension": 48,
    "Drug interaction": 45,
    "Dizziness": 40,
    "Bradycardia": 39,
    "Dyspnoea": 39,
    "Fatigue": 35,
    "Off label use": 34,
    "Diarrhoea": 33
  },
  "note": "No System Organ Class field is available in this dataset; analysis is at the Preferred Term level only."
}


## Serious Cases / 15-Day Alerts

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52dKZkDrGCGTA12FCEo'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'Serious Cases / 15-Day Alerts':]
{
  "reporting_period": {
    "start": "2024-12-27",
    "end": "2025-12-26"
  },
  "alert_15day": {
    "total_alert_cases": 1023,
    "alert_fatal_cases": 67
  },
  "case_volume": {
    "total_cases": 1024,
    "serious_cases": 1023,
    "non_serious_cases": 1,
    "serious_pct": 99.9
  }
}


## Trends and Important Observations

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52dP9J8dZbsY5hRD5G7'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'Trends and Important Observations':]
{
  "monthly_trend": {
    "2024-12": 21,
    "2025-01": 75,
    "2025-02": 94,
    "2025-03": 83,
    "2025-04": 78,
    "2025-05": 80,
    "2025-06": 84,
    "2025-07": 109,
    "2025-08": 64,
    "2025-09": 76,
    "2025-10": 102,
    "2025-11": 75,
    "2025-12": 83
  },
  "reporting_period": {
    "start": "2024-12-27",
    "end": "2025-12-26"
  }
}


## History of Actions

[LLM call failed: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011Ce52dSKJGYPNm6aFndqGk'}. Falling back to raw evidence.]
[Offline mode — no LLM call made. Raw evidence for 'History of Actions':]
{
  "history_of_actions": null
}


## Case Index / Listing (sample)

| Case ID | Reaction | Serious | Received | Country | Outcome |
|---|---|---|---|---|---|
| 24780403 | Rectal haemorrhage,Deficiency anaemia | serious | 20241227 | italy | unknown,unknown |
| 24780599 | Coma | serious | 20241227 | france | recovered/resolved |
| 24780680 | Acute kidney injury | serious | 20241227 | france | recovered/resolved |
| 24784771 | Muscle spasms | serious | 20241228 | united kingdom | recovered/resolved |
| 24784845 | Chest pain,Anxiety,Panic attack | serious | 20241228 | united kingdom | not recovered/not resolved/ongoing,recovering/resolving,recovering/resolving |
| 24784920 | Genital burning sensation | serious | 20241228 | united kingdom | not recovered/not resolved/ongoing |
| 24784985 | Pemphigoid | serious | 20241228 | united kingdom | unknown |
| 24784989 | Drug interaction,Hypersensitivity | serious | 20241228 | united kingdom | unknown,unknown |
| 24787006 | Bradycardia,Medication error | serious | 20241230 | united kingdom | not recovered/not resolved/ongoing,unknown |
| 24787240 | Muscle twitching,Muscle spasms | serious | 20241230 | united kingdom | not recovered/not resolved/ongoing,not recovered/not resolved/ongoing |
| 24787307 | Cardiac arrest | serious | 20241230 | united kingdom | recovering/resolving |
| 24787627 | Hypoglycaemia,Acidosis | serious | 20241230 | italy | recovering/resolving,recovering/resolving |
| 24788122 | Erectile dysfunction,Condition aggravated,Drug ineffective | serious | 20241230 | italy | recovering/resolving,recovering/resolving,unknown |
| 24791327 | Cardiac failure | serious | 20241231 | france | not recovered/not resolved/ongoing |
| 24791598 | Hepatic cytolysis | serious | 20241231 | france | recovering/resolving |
| 24791831 | Cardiogenic shock | serious | 20241231 | united kingdom | unknown |
| 24792345 | Atrioventricular block | serious | 20241231 | united kingdom | unknown |
| 24792691 | Pseudoporphyria | serious | 20241231 | france | recovering/resolving |
| 24792889 | Hyponatraemia,Hypervolaemia,Cardiac failure | serious | 20241231 | spain | recovered/resolved,recovered/resolved,recovered/resolved |
| 24793431 | Dyskinesia | serious | 20241231 | france | not recovered/not resolved/ongoing |

*Showing 20 of 1024 cases. Full listing available in the underlying dataset / case_index export.*


---
*Generated by a prototype system for the GenAR AI Engineering Challenge. Not a real regulatory submission. All figures traced to src/analysis.py output — see review_state.json for the human approval status of each section.*
