FITBIT_SCREENSHOT_PROMPT = """
Du analysierst einen Fitbit-Lauf-Screenshot.

Gib ausschließlich gültiges JSON zurück.

Schema:
{
  "kilometer": number | null,
  "dauer": number | null,
  "pace": string | null,
  "puls": number | null,
  "hoehenmeter": number | null,
  "kalorien": number | null
}

Regeln:
- kilometer als Dezimalzahl, z.B. 4.15
- dauer als Minuten-Dezimalzahl, z.B. 24.12 für 24 Minuten 7 Sekunden
- pace im Format MM:SS, z.B. "5:49"
- puls als bpm-Zahl
- kalorien als kcal-Zahl
- hoehenmeter falls nicht sichtbar: 0
- Keine Erklärung, kein Markdown, nur JSON.
"""