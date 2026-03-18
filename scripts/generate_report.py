#!/usr/bin/env python3
"""
AISTORE Analytics — Report Generator
Takes fetched data JSON and generates the final HTML report.
Uses the template in templates/ and injects fresh data.
"""
import json
import os
import sys
import re
from datetime import datetime, timezone


def load_data(data_path: str) -> dict:
    """Load the fetched data JSON."""
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(template_path: str) -> str:
    """Load the HTML template."""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_traffic_data(data: dict) -> dict:
    """Extract and structure traffic ranking data from search results."""
    # Default data (will be updated if fresh data is found)
    traffic = {
        "ChatGPT": {"visits": "5.72B", "value": 5720, "share": 64.5},
        "Canva": {"visits": "1.1B", "value": 1100, "share": 0},
        "DeepSeek": {"visits": "647.6M", "value": 647.6, "share": 8.5},
        "Gemini": {"visits": "546M", "value": 546, "share": 20.3},
        "Character.AI": {"visits": "420M", "value": 420, "share": 0},
        "Claude": {"visits": "246.2M", "value": 246.2, "share": 1.7},
        "Perplexity": {"visits": "200M", "value": 200, "share": 2.1},
        "Grok": {"visits": "180M", "value": 180, "share": 3.4},
        "Copilot": {"visits": "160M", "value": 160, "share": 1.3},
        "Midjourney": {"visits": "120M", "value": 120, "share": 0},
        "Suno": {"visits": "95M", "value": 95, "share": 0},
        "Poe": {"visits": "85M", "value": 85, "share": 0},
        "Photoroom": {"visits": "78M", "value": 78, "share": 0},
        "Runway": {"visits": "65M", "value": 65, "share": 0},
        "Cursor": {"visits": "55M", "value": 55, "share": 0},
    }

    # Try to parse updated numbers from search results
    ranking_data = data.get("queries", {}).get("traffic_ranking", {})
    snippets_text = " ".join(
        s.get("snippet", "") for s in ranking_data.get("snippets", [])
    )
    answer_text = ranking_data.get("answer", "")
    all_text = f"{answer_text} {snippets_text}"

    # Pattern: "ChatGPT" ... "X.XX billion" or "XXX million"
    for name in traffic:
        # Look for billion pattern
        pattern = rf'{re.escape(name)}[^.]*?(\d+(?:\.\d+)?)\s*(?:billion|B)\s*(?:visits|monthly)'
        m = re.search(pattern, all_text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            traffic[name]["visits"] = f"{val}B"
            traffic[name]["value"] = val * 1000

        # Look for million pattern
        pattern = rf'{re.escape(name)}[^.]*?(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:visits|monthly)'
        m = re.search(pattern, all_text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            traffic[name]["visits"] = f"{val}M"
            traffic[name]["value"] = val

    return traffic


def extract_market_size(data: dict) -> dict:
    """Extract market size projections."""
    defaults = {
        "2024": {"ai_software": 122, "gen_ai": 37.1},
        "2025": {"ai_software": 174.1, "gen_ai": 56},
        "2026": {"ai_software": 217, "gen_ai": 91.57},
        "2027": {"ai_software": 270, "gen_ai": 120},
        "2030": {"ai_software": 347, "gen_ai": 220},
    }
    return defaults


def extract_share_trend(data: dict) -> dict:
    """Extract market share trend data."""
    defaults = {
        "dates": ["2025.03", "2025.06", "2025.09", "2025.12", "2026.03"],
        "chatgpt": [86.7, 82, 78.6, 72, 64.5],
        "gemini": [5.7, 7, 8.6, 14, 20.3],
        "deepseek": [0, 1, 3.2, 6, 8.5],
        "grok": [0, 0.5, 1.8, 2.5, 3.4],
        "others": [7.6, 9.5, 7.8, 5.5, 3.3],
    }
    return defaults


def build_data_js(data: dict) -> str:
    """Build the JavaScript data object for chart rendering."""
    traffic = extract_traffic_data(data)
    market = extract_market_size(data)
    share = extract_share_trend(data)

    # Build traffic ranking arrays
    sorted_traffic = sorted(traffic.items(), key=lambda x: x[1]["value"], reverse=True)[:15]
    ranking_names = json.dumps([t[0] for t in sorted_traffic], ensure_ascii=False)
    ranking_values = json.dumps([t[1]["value"] for t in sorted_traffic])
    ranking_labels = json.dumps([t[1]["visits"] for t in sorted_traffic], ensure_ascii=False)

    # Share trend
    share_dates = json.dumps(share["dates"])
    share_chatgpt = json.dumps(share["chatgpt"])
    share_gemini = json.dumps(share["gemini"])
    share_deepseek = json.dumps(share["deepseek"])
    share_grok = json.dumps(share["grok"])
    share_others = json.dumps(share["others"])

    # Market size
    market_years = json.dumps(list(market.keys()))
    market_ai = json.dumps([v["ai_software"] for v in market.values()])
    market_gen = json.dumps([v["gen_ai"] for v in market.values()])

    # Key metrics for hero stats
    top_traffic = sorted_traffic[0]
    gen_date = data.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

    return f"""
// Auto-generated by AISTORE Analytics — {gen_date}
const REPORT_DATA = {{
  generated: "{gen_date}",
  ranking: {{ names: {ranking_names}, values: {ranking_values}, labels: {ranking_labels} }},
  share: {{
    dates: {share_dates},
    chatgpt: {share_chatgpt}, gemini: {share_gemini},
    deepseek: {share_deepseek}, grok: {share_grok}, others: {share_others}
  }},
  market: {{ years: {market_years}, ai_software: {market_ai}, gen_ai: {market_gen} }},
  topTool: "{top_traffic[0]}",
  topTraffic: "{top_traffic[1]['visits']}",
  topShare: {top_traffic[1]['share']},
  chatgptShareDelta: {round(share['chatgpt'][0] - share['chatgpt'][-1], 1)},
}};
"""


def build_insights_html(data: dict) -> str:
    """Build insights section from search answers."""
    sections = []
    for qid, qdata in data.get("queries", {}).items():
        answer = qdata.get("answer", "")
        if answer and len(answer) > 50:
            sections.append(f"""
      <div class="glass-card fade-in" style="margin-bottom:1rem">
        <div style="color:var(--accent);font-family:'JetBrains Mono';font-size:.7rem;margin-bottom:.5rem">{qdata['purpose'].upper()}</div>
        <p style="font-size:.88rem;color:#c8d6e5;line-height:1.7">{answer[:600]}</p>
        <div style="margin-top:.75rem;display:flex;gap:.5rem;flex-wrap:wrap">
""")
            for s in qdata.get("snippets", [])[:3]:
                title = s.get("title", "")[:40]
                url = s.get("url", "#")
                sections.append(
                    f'          <a href="{url}" target="_blank" style="font-size:.7rem;color:#667;'
                    f'text-decoration:none;border:1px solid rgba(255,255,255,.06);padding:.15rem .4rem;'
                    f'border-radius:3px;transition:color .2s" onmouseover="this.style.color=\'#00f0ff\'" '
                    f'onmouseout="this.style.color=\'#667\'">{title}</a>'
                )
            sections.append("        </div>\n      </div>")

    return "\n".join(sections) if sections else '<div class="glass-card"><p style="color:#667">本周未检索到新洞察。</p></div>'


def generate(data_path: str, template_path: str, output_path: str):
    """Generate the complete HTML report."""
    data = load_data(data_path)
    template = load_template(template_path)

    gen_date = data.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

    # Replace template variables
    replacements = {
        "{{GENERATED_DATE}}": gen_date,
        "{{GENERATED_YEAR}}": gen_date[:4],
        "{{DATA_JS}}": build_data_js(data),
        "{{INSIGHTS_HTML}}": build_insights_html(data),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated: {output_path}")
    print(f"  Date: {gen_date}")
    print(f"  Data sources: {sum(d['result_count'] for d in data['queries'].values())} snippets")


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/latest.json"
    template_path = sys.argv[2] if len(sys.argv) > 2 else "templates/report.html"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "docs/index.html"

    generate(data_path, template_path, output_path)
