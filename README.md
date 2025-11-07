# 🤖 Smart Support Triage (AI-Powered n8n Automation)

**Smart Support Triage** is an intelligent automation system built with [n8n](https://n8n.io/) that leverages AI to classify, score, and route incoming support messages. It assesses message complexity, assigns categories (Billing, Account, Bug, etc.), and decides whether to create a **Jira ticket**, post a **Slack** alert, or send an **email** summary—while logging every event to **PostgreSQL**.

> This project demonstrates real-world **AI + workflow orchestration** techniques used by Applied AI and Automation teams to reduce manual triage and accelerate response times.

---

## 🐳 Quick Start (Docker)

You can spin up a ready-to-run demo (with sample workflows auto-imported) in one command:

```bash
make up
```

- n8n and Postgres start automatically via Docker Compose  
- All workflows from `/workflows` are auto-imported  
- Open `http://localhost:5678` to explore  
- Run `make down` to stop or `make reset` for a clean rebuild  

> The `Makefile` provides shortcuts for common commands like `make up`, `make down`, `make logs`, and `make reset`. This makes the project immediately portable and simple for others to run.

---

## 🔑 Key Features

- 🔍 **AI-Powered Categorization**
  - Automatically classifies messages (Billing, Account, Technical, etc.)
  - Extracts summary and confidence score using OpenAI or Gemini models.

- 🧮 **Complexity Scoring**
  - Uses an AI model to assign a complexity score.
  - Scores drive routing: higher complexity = higher urgency.

- 🚦 **Automated Routing**
  - Complex & urgent → **Jira ticket**
  - Complex but non-urgent → **Slack alert**
  - Simple → **Email summary only**

- 🗂️ **Centralized Logging**
  - Logs all activity to **PostgreSQL** (or Google Sheets in early versions).
  - Includes AI metadata, confidence, and model token usage.

- 🧠 **Knowledge Search (RAG-ready)**
  - Integrates with Pinecone vector database to search knowledge base documentation and suggest fixes (sample knowledge base included under `docs/support_docs/`).

- 🧰 **Extensible Architecture**
  - Modular subflows: classification, routing, notification, logging, and error handling.
  - Ready for Docker, CI/CD, and deployment pipelines.

---

## 🧠 How It Works

```mermaid
graph TD;
    A[Webhook or Mock Data] --> B[OpenAI Classify & Summarize Incident];
    B --> C[RAG Knowledge Base Vector Search (AI Agent)];
    C --> D[Intelligent Routing];
    D --> E[Slack/Email/Jira Ticket];
    E --> F[PostgreSQL Log];
```

---

## ⚙️ Manual Setup (optional)

If you prefer to run n8n manually instead of Docker:

### 1️⃣ Prerequisites
- [Node.js](https://nodejs.org/) ≥ 18  
- [n8n](https://n8n.io/) ≥ 1.117 (self-hosted or desktop)  
- [PostgreSQL](https://www.postgresql.org/) or [Supabase](https://supabase.com/) instance  
- API keys for (see .env example for full list):
  - OpenAI (or Gemini)
  - Slack (Bot token)
  - Jira (API token)
  - Pinecone (optional, for RAG search)

### 2️⃣ Clone & Configure

```bash
git clone https://github.com/jbarnette93/smart-support-triage-n8n.git
cd smart-support-triage-n8n
cp .env.example .env
```

Then open `.env` and fill in your keys.

### 3️⃣ Create Env-Linked Credentials in n8n

In n8n → *Credentials*, create the following (exact names matter):

| Credential Name | Service | Fields / Values |
|------------------|----------|------------------|
| **OpenAi account** | OpenAI API | `API Key = {{$env.OPENAI_API_KEY}}` |
| **Slack account** | Slack Bot | `Token = {{$env.SLACK_BOT_TOKEN}}` |
| **Jira SW Cloud account** | Jira Cloud | `Email = {{$env.JIRA_BASE_EMAIL}}`, `Token = {{$env.JIRA_API_TOKEN}}`, `Domain = {{$env.JIRA_DOMAIN}}` |
| **Postgres account** | PostgreSQL / Supabase | `Host = {{$env.PG_HOST}}`, `User = {{$env.PG_USER}}`, `Password = {{$env.PG_PASSWORD}}`, `Database = {{$env.PG_DATABASE}}` |
| **SMTP account** | Email | `User = {{$env.SMTP_USER}}`, `Password = {{$env.SMTP_PASS}}` |
| **PineconeApi account** | Vector Search | `API Key = {{$env.PINECONE_API_KEY}}`, `Index = {{$env.PINECONE_INDEX}}` |

> 💡 *These credentials are linked to environment variables, so no secrets are stored inside n8n.*

---

## 🧩 Environment Variables

All variables are defined in `.env.example`.  
Do **not** commit `.env` — it’s included in `.gitignore`.  
Each variable name matches its use inside n8n nodes and credentials.  
The repo includes a `.env.example` for easy setup and a `.gitignore` that excludes real secrets.

---

## 🔐 Security & Privacy

- Never store API keys directly in nodes.
- Use `$env` variables and linked credentials.
- Sanitize test data before sharing.
- All logs redact customer identifiers.

---

## 🚀 Roadmap

| Phase | Focus |
|-------|--------|
| 1–4 | Core AI classification, routing, and error handling |
| 5 | Slack + Jira + Email + Sheets integration |
| 6 | OpenAI summarization & token tracking |
| 7 | Vector search & RAG integration |
| 8 | PostgreSQL persistence & environment refactor |
| 9 | Docker, cleanup, README polish, and GitHub release |

---

## 👤 Author

**Jonathan Barnette**  
*Data Automation / AI Automation Engineer*  
- GitHub: [jbarnette93](https://github.com/jbarnette93)  
- LinkedIn: [jonathan-barnette](https://www.linkedin.com/in/jonathan-barnette)

---

## 🧾 License

MIT License © 2025 — free to use, modify, and learn from.
