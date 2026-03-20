#!/usr/bin/env python3
"""
AISTORE Analytics — Agent Market Report Generator
Generates the Agent ecosystem analysis report from fetched data.
Five-layer analytical framework: PESTEL → Porter → Competitive Radar → Adoption Lifecycle → Blue Ocean
"""
import json
import os
import sys
from datetime import datetime


def load_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_agent_data_js(data: dict) -> str:
    """Build JS data object for agent report charts."""
    gen_date = data.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

    # --- Agent Market Size ---
    market = {
        "years": ["2024", "2025", "2026", "2027", "2030", "2033"],
        "size": [3.8, 7.84, 14.5, 24, 52.62, 182.97],
        "cagr": 46.3,
        "sources": ["MarketsandMarkets", "Grand View Research", "Yahoo Finance"]
    }

    # --- Competitor Matrix (multi-dimensional scores 0-100) ---
    competitors = {
        "names": ["TAAFT", "Toolify", "Futurepedia", "mcp.so", "mog.md",
                  "SkillsMP", "AI Agent Store", "HuggingFace", "GPT Store",
                  "Claude Marketplace", "AISTORE(目标)"],
        "dimensions": ["工具覆盖量", "数据分析", "安全审计", "Agent支持",
                       "MCP生态", "变现能力", "用户体验"],
        "scores": [
            [95, 30, 5,  10, 5,  60, 55],
            [85, 70, 5,  15, 10, 50, 60],
            [50, 20, 10, 10, 5,  45, 65],
            [15, 10, 5,  30, 90, 10, 40],
            [10, 5,  10, 40, 85, 80, 50],
            [20, 5,  5,  50, 80, 30, 45],
            [30, 10, 5,  60, 40, 20, 50],
            [90, 40, 15, 60, 30, 20, 70],
            [70, 15, 10, 30, 10, 40, 65],
            [15, 10, 20, 50, 50, 70, 60],
            [70, 85, 90, 85, 90, 75, 80],
        ],
        "traffic": {
            "TAAFT": "5M MAU", "Toolify": "1.5M", "Futurepedia": "800K",
            "mcp.so": "200K", "mog.md": "50K", "SkillsMP": "30K",
            "AI Agent Store": "20K", "HuggingFace": "32M",
            "GPT Store": "集成在ChatGPT", "Claude Marketplace": "新上线",
            "AISTORE(目标)": "目标1.2M"
        },
        "model": {
            "TAAFT": "付费收录$347", "Toolify": "Freemium $49-99",
            "Futurepedia": "收录$497+课程$30/mo", "mcp.so": "免费开源",
            "mog.md": "交易抽成Stripe", "SkillsMP": "免费索引GitHub",
            "AI Agent Store": "免费收录", "HuggingFace": "推理API收费",
            "GPT Store": "收入分成~$0.03/对话", "Claude Marketplace": "零佣金企业采购",
            "AISTORE(目标)": "安全审计+分发"
        }
    }

    # --- Porter's Five Forces scores (1-10) ---
    porter = {
        "dimensions": ["新进入者威胁", "替代品威胁", "买方议价能力",
                       "供应商议价能力", "行业竞争强度"],
        "scores": [8, 7, 6, 8, 9],
        "analysis": [
            "低进入壁垒，任何人都能建目录站，2026年2月28天内6家agent marketplace上线",
            "大厂自建生态(Claude Marketplace, GPT Store)可替代独立平台",
            "开发者和企业有多个平台选择，转换成本低",
            "依赖AI厂商API和模型，OpenAI/Anthropic控制核心资源",
            "从目录站到agent marketplace，所有玩家同时涌入，竞争白热化"
        ]
    }

    # --- Technology Adoption Lifecycle ---
    lifecycle = {
        "stages": ["创新者", "早期采用者", "早期多数", "晚期多数", "落后者"],
        "technologies": [
            {"name": "A2A Protocol", "stage": 0, "maturity": 15},
            {"name": "Agent Skills (.skill.md)", "stage": 0, "maturity": 20},
            {"name": "Multi-Agent框架", "stage": 1, "maturity": 35},
            {"name": "MCP Protocol", "stage": 1, "maturity": 40},
            {"name": "Agent Marketplace", "stage": 1, "maturity": 30},
            {"name": "AI Agent (单体)", "stage": 2, "maturity": 55},
            {"name": "RAG/知识库", "stage": 2, "maturity": 60},
            {"name": "LLM API", "stage": 3, "maturity": 80},
            {"name": "AI聊天机器人", "stage": 3, "maturity": 85},
        ]
    }

    # --- Blue Ocean: AISTORE vs Incumbents ---
    blue_ocean = {
        "factors": ["工具数量", "流量SEO", "数据分析", "安全审计",
                    "一键部署", "Agent/MCP", "变现生态", "企业合规"],
        "taaft":    [9, 10, 3, 1, 1, 1, 6, 1],
        "toolify":  [8, 8, 7, 1, 1, 2, 5, 1],
        "huggingface": [9, 7, 4, 2, 6, 3, 3, 3],
        "aistore":  [7, 5, 9, 10, 9, 10, 8, 9],
    }

    # --- Agent Framework Ecosystem ---
    frameworks = [
        {"name": "LangChain/LangGraph", "type": "开源框架", "stars": "98K+", "focus": "全功能Agent编排"},
        {"name": "CrewAI", "type": "开源框架", "stars": "25K+", "focus": "多Agent协作"},
        {"name": "AutoGen/AG2", "type": "微软开源", "stars": "40K+", "focus": "对话式多Agent"},
        {"name": "OpenAI Agents SDK", "type": "官方SDK", "stars": "-", "focus": "轻量Agent工具"},
        {"name": "Google ADK", "type": "官方SDK", "stars": "-", "focus": "Gemini生态Agent"},
        {"name": "Claude Agent SDK", "type": "官方SDK", "stars": "-", "focus": "MCP原生Agent"},
        {"name": "Mastra", "type": "开源框架", "stars": "10K+", "focus": "TypeScript Agent"},
        {"name": "Pydantic AI", "type": "开源框架", "stars": "8K+", "focus": "类型安全Agent"},
    ]

    return f"""
// Auto-generated by AISTORE Agent Analytics — {gen_date}
const AGENT_DATA = {{
  generated: "{gen_date}",
  market: {json.dumps(market, ensure_ascii=False)},
  competitors: {json.dumps(competitors, ensure_ascii=False)},
  porter: {json.dumps(porter, ensure_ascii=False)},
  lifecycle: {json.dumps(lifecycle, ensure_ascii=False)},
  blueOcean: {json.dumps(blue_ocean, ensure_ascii=False)},
  frameworks: {json.dumps(frameworks, ensure_ascii=False)},
}};
"""


def build_agent_insights_html(data: dict) -> str:
    """Build insights from agent-specific search results."""
    agent_qids = ["agent_market_size", "agent_frameworks", "agent_marketplaces",
                  "agent_competitors", "agent_trends", "agent_china"]
    sections = []
    for qid in agent_qids:
        qdata = data.get("queries", {}).get(qid, {})
        answer = qdata.get("answer", "")
        if answer and len(answer) > 50:
            sections.append(f"""
      <div class="glass-card fade-in" style="margin-bottom:1rem">
        <div style="color:var(--accent);font-family:'JetBrains Mono';font-size:.7rem;margin-bottom:.5rem">{qdata.get('purpose', qid).upper()}</div>
        <p style="font-size:.88rem;color:#c8d6e5;line-height:1.7">{answer[:800]}</p>
        <div style="margin-top:.75rem;display:flex;gap:.5rem;flex-wrap:wrap">""")
            for s in qdata.get("snippets", [])[:4]:
                title = s.get("title", "")[:50]
                url = s.get("url", "#")
                sections.append(
                    f'          <a href="{url}" target="_blank" style="font-size:.7rem;color:#667;'
                    f'text-decoration:none;border:1px solid rgba(255,255,255,.06);padding:.15rem .4rem;'
                    f'border-radius:3px;transition:color .2s" onmouseover="this.style.color=\'#00f0ff\'" '
                    f'onmouseout="this.style.color=\'#667\'">{title}</a>')
            sections.append("        </div>\n      </div>")
    return "\n".join(sections) if sections else '<div class="glass-card"><p style="color:#667">本周未检索到Agent市场新洞察。</p></div>'


def generate(data_path: str, template_path: str, output_path: str):
    data = load_data(data_path)
    template = load_template(template_path)
    gen_date = data.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

    replacements = {
        "{{GENERATED_DATE}}": gen_date,
        "{{GENERATED_YEAR}}": gen_date[:4],
        "{{AGENT_DATA_JS}}": build_agent_data_js(data),
        "{{AGENT_INSIGHTS_HTML}}": build_agent_insights_html(data),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Agent report generated: {output_path}")
    print(f"  Date: {gen_date}")
    agent_qids = ["agent_market_size", "agent_frameworks", "agent_marketplaces",
                  "agent_competitors", "agent_trends", "agent_china"]
    total = sum(data.get("queries", {}).get(q, {}).get("result_count", 0) for q in agent_qids)
    print(f"  Agent data sources: {total} snippets")


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/latest.json"
    template_path = sys.argv[2] if len(sys.argv) > 2 else "templates/agent-report.html"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "docs/agent.html"
    generate(data_path, template_path, output_path)
