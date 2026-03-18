#!/usr/bin/env python3
"""
AISTORE Analytics — Data Fetcher
Fetches latest AI market data from Tavily API and outputs structured JSON.
Designed to run in GitHub Actions or locally.
"""
import json
import os
import sys
import time
import re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

QUERIES = [
    {
        "id": "traffic_ranking",
        "query": "top AI websites traffic ranking monthly visits 2025 2026 ChatGPT Gemini DeepSeek Claude Perplexity",
        "purpose": "AI tool traffic rankings"
    },
    {
        "id": "market_share",
        "query": "AI chatbot market share traffic percentage ChatGPT Gemini DeepSeek 2026",
        "purpose": "Market share trends"
    },
    {
        "id": "market_size",
        "query": "generative AI market size forecast 2026 2027 2030 revenue growth",
        "purpose": "Market size projections"
    },
    {
        "id": "trends",
        "query": "AI industry trends 2026 agentic AI MCP protocol enterprise adoption",
        "purpose": "Key market trends"
    },
    {
        "id": "mcp_ecosystem",
        "query": "MCP model context protocol ecosystem tools servers 2025 2026 growth",
        "purpose": "MCP ecosystem updates"
    },
    {
        "id": "competitors",
        "query": "AI tools directory aggregator platform TAAFT toolify futurepedia there is an AI for that traffic",
        "purpose": "Competitor landscape"
    },
    {
        "id": "chinese_market",
        "query": "AI网站流量排名 2026 中国AI工具 DeepSeek 百度AI 访问量",
        "purpose": "Chinese market data"
    },
    {
        "id": "user_behavior",
        "query": "AI tool usage statistics user behavior popular features coding image generation 2025 2026",
        "purpose": "User behavior patterns"
    }
]


def search_tavily(query: str, max_results: int = 8) -> dict:
    """Search using Tavily API."""
    if not TAVILY_API_KEY:
        return {"error": "TAVILY_API_KEY not set", "results": []}

    payload = json.dumps({
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": True
    }).encode()

    req = Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        },
        method="POST"
    )

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError) as e:
        return {"error": str(e), "results": []}


def search_serper(query: str, max_results: int = 8) -> dict:
    """Search using Serper API (fallback)."""
    if not SERPER_API_KEY:
        return {"error": "SERPER_API_KEY not set", "results": []}

    payload = json.dumps({
        "q": query,
        "num": max_results
    }).encode()

    req = Request(
        "https://google.serper.dev/search",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": SERPER_API_KEY
        },
        method="POST"
    )

    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            # Normalize to common format
            results = []
            for item in data.get("organic", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "content": item.get("snippet", "")
                })
            return {"results": results, "answer": data.get("answerBox", {}).get("answer", "")}
    except (URLError, HTTPError) as e:
        return {"error": str(e), "results": []}


def fetch_all() -> dict:
    """Fetch data for all queries."""
    timestamp = datetime.now(timezone.utc).isoformat()
    data = {
        "generated_at": timestamp,
        "generated_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "queries": {}
    }

    provider = "tavily" if TAVILY_API_KEY else "serper"
    search_fn = search_tavily if TAVILY_API_KEY else search_serper

    print(f"Using provider: {provider}")
    print(f"Fetching {len(QUERIES)} data categories...\n")

    for i, q in enumerate(QUERIES):
        print(f"  [{i+1}/{len(QUERIES)}] {q['purpose']}...")
        result = search_fn(q["query"])

        if "error" in result and not result.get("results"):
            print(f"    ⚠ Error: {result['error']}")
            # Try fallback provider
            if provider == "tavily" and SERPER_API_KEY:
                print(f"    → Trying serper fallback...")
                result = search_serper(q["query"])

        snippets = []
        for r in result.get("results", []):
            snippets.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", r.get("snippet", ""))[:500]
            })

        data["queries"][q["id"]] = {
            "purpose": q["purpose"],
            "query": q["query"],
            "answer": result.get("answer", ""),
            "result_count": len(snippets),
            "snippets": snippets
        }

        # Rate limit protection
        if i < len(QUERIES) - 1:
            time.sleep(1)

    print(f"\nDone. {sum(d['result_count'] for d in data['queries'].values())} total results collected.")
    return data


def extract_numbers(text: str) -> list:
    """Extract numeric values from text for data points."""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:billion|B)\b',
        r'(\d+(?:\.\d+)?)\s*(?:million|M)\b',
        r'(\d+(?:\.\d+)?)\s*%',
        r'\$(\d+(?:\.\d+)?)\s*(?:billion|B)',
    ]
    numbers = []
    for p in patterns:
        numbers.extend(re.findall(p, text, re.IGNORECASE))
    return numbers


if __name__ == "__main__":
    output_path = sys.argv[1] if len(sys.argv) > 1 else "data/latest.json"

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    data = fetch_all()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_path}")
