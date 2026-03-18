# AISTORE Analytics — AI 市场自动分析系统

每周自动搜索最新 AI 市场数据，生成可视化分析报告，部署到 GitHub Pages。

## 快速开始

### 1. Fork 本仓库

### 2. 配置 API Key

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret | 说明 | 获取地址 |
|--------|------|----------|
| `TAVILY_API_KEY` | **必需** - Tavily 搜索 API | [tavily.com](https://tavily.com) |
| `SERPER_API_KEY` | 可选 - Serper 搜索 API（备用） | [serper.dev](https://serper.dev) |

### 3. 启用 GitHub Pages

Settings → Pages → Source: GitHub Actions

### 4. 手动触发首次运行

Actions → Weekly AI Market Report → Run workflow

---

## 项目结构

```
aistore-analytics/
├── .github/workflows/
│   └── weekly-report.yml    # 每周一 08:00 UTC 自动运行
├── scripts/
│   ├── fetch_data.py        # 数据采集（Tavily/Serper API）
│   └── generate_report.py   # 报告生成（数据注入 HTML 模板）
├── templates/
│   ├── report.html          # 分析报告模板（含 ECharts 可视化）
│   └── aistore-website.html # AISTORE 品牌官网
├── data/
│   ├── latest.json          # 最新一期数据
│   └── archive/             # 历史数据存档
├── docs/                    # GitHub Pages 部署目录
│   └── index.html           # 生成的报告（自动更新）
└── README.md
```

## 工作原理

1. **数据采集** — `fetch_data.py` 通过 Tavily API 搜索 8 个维度的最新 AI 市场数据
2. **数据存档** — 每期数据保存为 JSON，支持历史对比
3. **报告生成** — `generate_report.py` 将数据注入 HTML 模板，生成可视化报告
4. **自动部署** — GitHub Actions 将报告推送到 `docs/`，GitHub Pages 自动发布

## 手动运行

```bash
# 安装依赖（无第三方依赖，仅需 Python 3.8+）

# 1. 设置 API Key
export TAVILY_API_KEY="tvly-xxxxx"

# 2. 采集数据
python scripts/fetch_data.py data/latest.json

# 3. 生成报告
python scripts/generate_report.py data/latest.json templates/report.html docs/index.html

# 4. 本地预览
cd docs && python -m http.server 8080
```

## 数据维度

| 维度 | 说明 |
|------|------|
| traffic_ranking | AI 工具全球流量排名 Top 15 |
| market_share | ChatGPT/Gemini/DeepSeek 等市场份额变化 |
| market_size | 生成式 AI 市场规模预测 |
| trends | Agentic AI、MCP 生态等关键趋势 |
| mcp_ecosystem | MCP/Skills 生态最新动态 |
| competitors | 竞品平台（TAAFT、Toolify 等）动态 |
| chinese_market | 中国 AI 市场数据 |
| user_behavior | 用户行为和功能偏好 |

## 自定义

### 修改搜索查询
编辑 `scripts/fetch_data.py` 中的 `QUERIES` 列表。

### 修改报告样式
编辑 `templates/report.html`，保留 `{{DATA_JS}}` 等模板变量。

### 修改更新频率
编辑 `.github/workflows/weekly-report.yml` 中的 cron 表达式：
- 每周一: `0 8 * * 1`
- 每天: `0 8 * * *`
- 每月1号: `0 8 1 * *`

## 技术栈

- **数据采集**: Python 3 (标准库，无第三方依赖)
- **搜索 API**: Tavily (主) / Serper (备)
- **可视化**: ECharts 5 (SVG)
- **动画**: GSAP + ScrollTrigger
- **样式**: TailwindCSS + 自定义 Neon Noir 主题
- **字体**: Noto Sans SC + JetBrains Mono + Playfair Display
- **部署**: GitHub Actions + GitHub Pages

---

**AISTORE** — 发现 · 连接 · 运行可信 AI
