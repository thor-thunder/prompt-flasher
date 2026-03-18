# 🧠 Prompt Generator
**by The Missing Link (thor-thunder)**

> Generate expert-level, copy-paste-ready prompts for any AI platform — powered by DSPy + OpenRouter. 🚀

---

## 📋 License

This project is released under the **MIT License** — free to use, modify, and distribute. See `LICENSE` for full text.

---

## ⚙️ Setup

### Step 1 — Create a virtual environment 🐍

============================
python3 -m venv venv
============================

---

### Step 2 — Activate the venv 🔌

**🐧💻 Linux / Mac**

On Arch Linux or any fish shell:

============================
source venv/bin/activate.fish
============================

OR

On Ubuntu, Debian or any bash/zsh shell:

============================
source ./venv/bin/activate
============================

---

**🪟 Windows**

In Command Prompt (cmd.exe):

============================
venv\Scripts\activate.bat
============================

OR

In PowerShell:

============================
.\venv\Scripts\Activate.ps1
============================

> 💡 If PowerShell blocks the script, run this first:
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

---

### Step 3 — Install requirements 📦

Once the venv is active, run:

============================
pip install -r requirements.txt
============================

---

### Step 4 — Configure your API key 🔑

Edit `.env` and paste your OpenRouter key:

============================
OPENROUTER_API_KEY=sk-or-v1-...
============================

Get a free key at 👉 https://openrouter.ai

---

## ▶️ Run

After setup, just double-click or run:

**🐧💻 Linux / Mac**
============================
./start.sh
============================

**🪟 Windows**
============================
start.cmd
============================

Then open your browser → http://localhost:3000 🌐

> 💡 The start scripts are self-healing — on a fresh machine they will automatically create the venv and install all dependencies before launching.

---

## 🤖 Generator Models

Choose which AI generates your prompt — all routed through OpenRouter with a single API key:

| Model | Notes |
|---|---|
| **AutoRouter** ⭐ FREE | Default. OpenRouter picks the best available model automatically. |
| **Claude Sonnet 4.6** | Best for complex reasoning, long-form writing, and nuanced instructions. |
| **Gemini 3 Flash** | Fast and capable. Great for structured and multimodal prompts. |
| **Nemotron 49B v1.5** | NVIDIA's high-reasoning model, great for technical and agentic tasks. |
| **MiniMax M2.5** | Fast, multilingual, strong on creative and conversational outputs. |
| **o4-mini** | OpenAI reasoning model. Precise and methodical. |
| **DeepSeek V3.2** | Excellent for code-heavy and technical prompt engineering. |

---

## 🔧 How it works

1. ✍️ You type your goal
2. 🔍 **DSPy AnalyzeGoal** — extracts intent, audience, tone, constraints
3. ✨ **DSPy CraftPrompt** — builds an expert prompt tuned for your target platform
4. 📋 Copy and paste into Claude / ChatGPT / Grok / Gemini / Midjourney / DeepSeek

---

*Made with ❤️ by The Missing Link (thor-thunder) — free for everyone.*
