import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_detection_rules(threat_description: str, mitre_id: str = "") -> dict:
    """
    Takes a threat description and optional MITRE ATT&CK ID.
    Returns detection rules in Sigma, Splunk SPL, KQL, and Wazuh XML formats.
    """

    mitre_context = f"MITRE ATT&CK Technique: {mitre_id}" if mitre_id else ""

    prompt = f"""You are a senior detection engineer. Generate detection rules for the following threat.

Threat Description: {threat_description}
{mitre_context}

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation outside JSON):

{{
  "threat_summary": "One sentence describing what this rule detects",
  "mitre_technique": "T1XXX.XXX — Technique Name",
  "severity": "Critical | High | Medium | Low",
  "false_positive_notes": "Brief notes on likely false positives",
  "sigma": "Complete Sigma YAML rule here as a string",
  "splunk_spl": "Complete Splunk SPL search query here",
  "kql": "Complete KQL query for Microsoft Sentinel here",
  "wazuh_xml": "Complete Wazuh XML detection rule here"
}}

Rules for each format:

SIGMA: Must include title, id (generate a UUID), status, description, references, author, date, logsource, detection (keywords/condition), falsepositives, level fields.

SPLUNK SPL: Must be a complete, runnable SPL search with index, sourcetype, field filters, stats or eval as appropriate.

KQL: Must be valid KQL for Microsoft Sentinel, referencing appropriate tables (SecurityEvent, Sysmon, etc.).

WAZUH XML: Must be valid Wazuh rule XML with rule id, level, description, and appropriate field matches.

Be specific and technically accurate. Use real field names for each platform."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)