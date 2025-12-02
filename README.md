# 📚 Multi-Agent Research System (Powered by Google ADK)

A fully modular, agentic research assistant built on **Google’s Agent Developer Kit (ADK)**.
Designed for **high-accuracy academic research**, scientific extraction, iterative reasoning, contradiction detection, and structured synthesis.

This system aims to surpass typical AI research assistants (Gemini Research, Perplexity, Elicit) by using:

- **Multi-Agent Architecture**
- **Reflection Loops**
- **Evidence-Linked Extraction**
- **Persistent Memory**
- **Tool-Augmented Reasoning**
- **Front-end Control Panel**

---

# 🧠 Project Goals

This system is designed to:

✔ Parse vague research topics into structured queries
✔ Perform reliable scientific web search
✔ Extract structured insights from web articles / PDFs
✔ Validate claims with evidence passages
✔ Detect contradictions across multiple sources
✔ Run iterative loops until quality thresholds are met
✔ Generate accurate summaries, reports, and experiment plans
✔ Maintain memory to grow smarter over time
✔ Provide an interactive dashboard to control agents

---

# 📐 System Architecture

The entire system follows a **multi-agent pipeline**, orchestrated automatically by ADK.

```
User Input
   ↓
QueryParserAgent
   ↓
RetrieverAgent (Search + Browser)
   ↓
DocProcessorAgent
   ↓
PaperReaderAgent
   ↓
CriticAgent
   ↓
LoopManagerAgent (Reflection, optional)
   ↓
InsightSynthesizerAgent
   ↓
FormatterAgent
   ↓
Final Output
```

### ✨ Key Highlights

- **Each agent has a single responsibility** → reliable + modular
- **ADK orchestrator automatically routes tasks**
- **Reflection loop improves accuracy**
- **JSON-only communication ensures deterministic behavior**
- **Memory stores user preferences + past research**
- **Frontend shows live agent progress**

---

# 🧩 Agent Responsibilities (Technical Breakdown)

### **1️⃣ QueryParserAgent**
Converts user topic → structured research query.

Outputs JSON with:
- core question
- sub-questions
- keywords
- boolean search queries
- desired outputs (summary/report/experiment plan)

---

### **2️⃣ RetrieverAgent**
Uses **Search Tool + WebBrowser Tool** to gather documents.

Outputs:
- title
- url
- snippet
- raw extracted content
- relevance score

---

### **3️⃣ DocProcessorAgent**
Processes raw content:
- removes boilerplate
- extracts main article body
- sections text (intro/method/results/etc.)
- chunks text for structured parsing

---

### **4️⃣ PaperReaderAgent**
Extracts structured scientific information:
- problem statement
- methods
- results + numbers
- claims
- limitations
- evidence quotes

---

### **5️⃣ CriticAgent**
Evaluates quality:
- flags contradictions
- checks unsupported claims
- rates source reliability
- requests additional search (via loop)

---

### **6️⃣ LoopManagerAgent** *(optional but powerful)*
Controls iterative improvement:
- reruns Retriever or Reader
- improves recall + reduces hallucination

---

### **7️⃣ InsightSynthesizerAgent**
Synthesizes results:
- research gaps
- insights
- hypotheses
- experiment suggestions

Uses validated evidence only.

---

### **8️⃣ FormatterAgent**
Creates final output:
- 1-page summary
- detailed research report
- bullet insights
- bibliography
- experiment checklist

---

# 🏛 Folder Structure

```
research-agent/
│
├── backend/
│   ├── adk/
│   │   ├── agents/
│   │   │   ├── query_parser/
│   │   │   ├── retriever/
│   │   │   ├── doc_processor/
│   │   │   ├── paper_reader/
│   │   │   ├── critic/
│   │   │   ├── loop_manager/
│   │   │   ├── synthesizer/
│   │   │   └── formatter/
│   │   │
│   │   ├── tools/
│   │   │   ├── search_tool.py
│   │   │   ├── browser_tool.py
│   │   │   └── pdf_processor.py
│   │   │
│   │   ├── workflows/
│   │   │   └── research_graph.json
│   │   │
│   │   ├── memory/
│   │   │   ├── embeddings/
│   │   │   ├── vector_store.faiss
│   │   │   └── prefs.json
│   │   │
│   │   ├── api/
│   │   │   ├── index.py
│   │   │   ├── routes/
│   │   │   └── utils/
│   │   │
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── styles/
│   │
│   ├── public/
│   └── package.json
│
├── docker-compose.yaml
├── .env
└── README.md
```

All empty folders contain `.gitkeep` so Git doesn’t ignore them.

---

# 💡 Frontend Features

The React-based frontend provides:

- Input box for research topic
- Live agent execution timeline
- Real-time tool results
- Insights panel
- Paper list panel
- Final formatted output
- Dark theme for focus
- "Re-run with refined query" control

---

# 🛠 Backend API Endpoints

### `POST /run_research`
Starts the full multi-agent research pipeline.
Returns **Server-Sent Events** updates as agents progress.

### `GET /status/<task_id>`
Returns current execution status.

### `POST /memory/update`
Save user preferences.

---

## 🚀 How to Run the Project (Beginner-Friendly Guide)

This project has **two modes of operation**:

1. **Full ADK Multi-Agent Pipeline** (uses ADK Runner, Sessions, multiple agents)
2. **Python-Only Retriever Pipeline** (no ADK, faster for testing)

Choose the mode you want and follow the instructions below.

---

# ✅ OPTION A — Full Multi-Agent System (ADK Orchestrator)

This mode runs the actual multi-agent pipeline:
`QueryParser → Retriever → DocProcessor → Reader → Critic → Synthesizer → Formatter`

### 1️⃣ Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

Make sure your .env contains valid keys:

GEMINI_API_KEY=your_key
SCRAPERAPI_KEY=your_key

### 2 Run Orchestrator
```bash
python -m app_adk.orchrestrator
```


## Future Plans
## 🔮 Future of the Project

This project was originally designed to be a **fully modular, production-grade multi-agent research system**.
Even though the current version uses a simplified Python pipeline, the following expansions remain planned and supported.

---

# 🖥️ Frontend (Planned)

The frontend is intended to give users a clean, interactive research dashboard.

### 🌐 Planned Features
- Real-time agent execution timeline
- Visual debugging of every agent’s output
- Document viewer (webpages, PDFs, research papers)
- Search results panel with link previews
- Evidence tracking (highlighted quotes)
- Insight panel and auto-generated summary
- Button to rerun pipeline with refined queries
- Light / Dark theme
- Workspace history with past research tasks

### 🧩 Planned Tech Stack
- React + Vite
- TailwindCSS
- State management (Zustand or Redux Toolkit)
- SSE or WebSockets for live agent updates
- API wrapper for backend ADK orchestrator

---

# 🐳 Docker Support (Planned)

The goal is **one-command deployment** through Docker.



# 🧱 Tech Stack

| Layer | Tools |
|-------|-------|
| Orchestration | **Google ADK** |
| Backend | Python, FastAPI |
| Tools | Search, Browser, Python |
| Memory | FAISS / pgvector |
| Frontend | React + Vite + Tailwind |
| Deployment | Docker + docker-compose |

---

# 🧠 Why This Beats Standard Research AI Tools

This system:
- Uses **multiple specialist agents**, not one monolithic LLM
- Has **reflection loops** for accuracy
- Uses **structured JSON extraction**, not free text
- Has **persistent memory**
- Allows **tool-augmented logic**
- Provides **full transparency & debugging**
- Offers a **custom UI** for control
- Can import/export workflows and plug in other LLMs

---

# 🧩 Teammate Onboarding Notes

### **Agent Development Rules**
1. Only modify your agent folder:
   ```
   backend/adk/agents/<agent_name>/
   ```
2. Follow JSON schemas strictly
3. Respect tool permissions in `config.yaml`
4. Do NOT change downstream agent contracts
5. Always test your agent individually in ADK UI

---

# 📈 Roadmap

- PDF scraping
- Jupyter notebook auto-generation
- Dataset ingestion + analysis tools
- Notion/Obsidian export
- Multi-user workspace with authentication
- Research project memory graph
- Fine-tuned extraction models

---

# ❤️ Author Note

This project is designed to be a **real personal research companion** —
not just another LLM wrapper.
Every part is intentionally modular, so your team can extend it based on your university/industry needs.
