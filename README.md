🌟 AI Agent Project with n8n

A fully functional AI-powered automation system built using a modern frontend and an n8n workflow-driven backend. This project demonstrates how an intelligent agent can receive user input, process it through AI models, trigger workflows, and return structured, meaningful results — all inside an elegant web interface.

🚀 Overview

This project integrates:

A React + Vite + Tailwind frontend

A backend powered by n8n (AI Agent + workflow automation)

Webhooks for seamless communication

AI capabilities for reasoning, summarization, and automated task execution

It is designed as a module-based AI agent system where your frontend sends data → n8n processes it through an AI workflow → responds back to the client.

🧠 Key Features
🔹 Intelligent AI Processing

Uses n8n’s AI Agent node, LLMs, and custom tools to process text, extract insights, and automate decisions.

🔹 Workflow-Driven Architecture

All backend logic is handled visually inside n8n workflows — easy to modify, extend, and scale.

🔹 Clean & Modern Frontend

A fully responsive UI supporting chat interactions, message streaming, loading states, and more.

🔹 Extensible and Modular

Add new tools to your AI agent (Web scraping, API calls, database queries, emails, etc.) without modifying backend code — just update n8n workflows.

📁 Project Structure
📦 AI-Agent-Project-with-n8n
│
├── 📂 Frontend             # React / Vite / Tailwind UI
│   ├── src/components      # Modular UI components
│   ├── src/pages           # App pages (Chat, Home, 404, etc.)
│   ├── public              # Assets
│   └── ...config files
│
├── 📂 n8n-workflows        # Exported workflows (optional)
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/iqbal-mih/-AI-Agent-Project-with-n8n.git
cd -AI-Agent-Project-with-n8n

2️⃣ Setup Frontend

Navigate into the frontend folder:

cd Frontend
bun install   # or npm install / pnpm install


Start development server:

bun dev       # or npm run dev


Your app will be live at:

http://localhost:3000

3️⃣ Setup n8n (Backend)
Option A — Run n8n locally
npx n8n


Access the Editor UI:

http://localhost:5678

Option B — Use n8n Cloud

Import your workflows directly into your cloud workspace.

🔗 Connecting Frontend & n8n

Your frontend sends requests to an n8n Webhook Trigger node:

Frontend → Backend (FastAPI or direct) → n8n Workflow → AI Agent → Response → Frontend


You must place your webhook URL in:

.env


Example:

VITE_N8N_WEBHOOK_URL=https://your-n8n-url.com/webhook/agent

🧩 Workflow Example

A typical n8n workflow looks like:

Webhook Trigger
      ↓
AI Agent (LLM reasoning + tool selection)
      ↓
Function / HTTP / API Calls
      ↓
Return Response to Frontend


This architecture allows your AI agent to analyze input, select tools, and automate tasks — fully controlled visually through n8n.

🎨 Frontend Features

✨ Chat interface (messages, bubbles, timestamps)

✨ Typing indicators

✨ Auto-scroll

✨ Shadcn/UI components

✨ Clean and smooth UX

🛡️ Environment Variables

Create a .env file:

VITE_N8N_WEBHOOK_URL=<your_n8n_webhook>
OPENAI_API_KEY=<your_api_key>


Add more depending on your workflow tools.

🧪 Running the Full System
Step 1 → Start n8n
Step 2 → Start the frontend
Step 3 → Trigger workflow from UI
Step 4 → Observe AI responses in the chat interface
📦 Build for Production
bun run build


Output will be generated in:

Frontend/dist


Host it on Vercel, Netlify, or any CDN-based provider.

🤝 Contributing

Pull requests are welcome!
You can help improve:

Frontend UI

Workflow logic

Documentation

Deployment setup

Additional AI tools

📜 License

MIT License — feel free to use this project for personal or commercial work.

👤 Author

Iqbal
AI & Workflow Automation Enthusiast
Feel free to reach out for collaboration or improvements!
