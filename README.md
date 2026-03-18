# 🧠 Prompt Generator

> Generate expert-level, copy-paste-ready prompts for any AI platform — powered by DSPy + OpenRouter.

**by [The Missing Link (thor-thunder)](https://github.com/thor-thunder)**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## What it does

1. ✍️ You type your goal
2. 🔍 **DSPy AnalyzeGoal** — extracts intent, audience, tone, and constraints
3. ✨ **DSPy CraftPrompt** — builds an expert prompt tuned for your target platform
4. 📋 Copy and paste into Claude / ChatGPT / Grok / Gemini / Midjourney / DeepSeek

---

## Quick Start

> **TL;DR:** Clone the repo, set your API key in `.env`, and run the start script.

### 1. Clone & enter the project

```bash
git clone https://github.com/thor-thunder/prompt-generator.git
cd prompt-generator
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**Linux / Mac**

```bash
# fish shell (Arch Linux, etc.)
source venv/bin/activate.fish

# bash / zsh (Ubuntu, Debian, etc.)
source ./venv/bin/activate
```

**Windows**

```bat
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
.\venv\Scripts\Activate.ps1
```

> 💡 If PowerShell blocks the script, run this first:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your API key

Rename `example.env` to `.env`, then open it and paste your OpenRouter key.
Get one for free at **https://www.openrouter.ai**

```bash
mv example.env .env
```

```env
OPENROUTER_API_KEY=sk-or-v1-...
```

### 6. Run

**Linux / Mac**
```bash
./start.sh
```

**Windows**
```bat
start.cmd
```

Then open your browser at **http://localhost:3000**

> 💡 The start scripts are self-healing — on a fresh machine they automatically create the venv and install all dependencies before launching.

---

## Generator Models

All models are routed through OpenRouter with a single API key.

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

## License

Released under the **MIT License** — free to use, modify, and distribute. See [`LICENSE`](LICENSE) for full text.

---

*Made with ❤️ by The Missing Link (thor-thunder) — free for everyone.*
